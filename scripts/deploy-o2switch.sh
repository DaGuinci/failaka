#!/bin/bash

# Script de déploiement local pour O2switch
# Utilise les mêmes étapes que le workflow GitHub Actions

set -e

echo "🚀 Déploiement Failaka vers O2switch"
echo "======================================"

# Configuration (à personnaliser)
SFTP_HOST="${O2SWITCH_SFTP_HOST:-votre-domaine.o2switch.net}"
SFTP_USER="${O2SWITCH_SFTP_USERNAME:-github-deploy}"
SFTP_PORT="${O2SWITCH_SFTP_PORT:-21}"
DEPLOY_DIR="deploy-package"

# Vérifier que les variables d'environnement sont définies
if [ -z "$O2SWITCH_SFTP_PASSWORD" ]; then
    echo "❌ Erreur: Variable O2SWITCH_SFTP_PASSWORD non définie"
    echo "💡 Exportez la variable: export O2SWITCH_SFTP_PASSWORD='votre_mot_de_passe'"
    exit 1
fi

# 1. Build des assets
echo "📦 Build des assets SCSS..."
npm run build

# 2. Collecte des fichiers statiques Django
echo "📂 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# 3. Création du package de déploiement
echo "📋 Création du package de déploiement..."
rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR

# Copier les fichiers Python/Django
echo "📁 Copie des modules Django..."
cp -r authentication/ $DEPLOY_DIR/
cp -r client/ $DEPLOY_DIR/
cp -r entities/ $DEPLOY_DIR/
cp -r failaka/ $DEPLOY_DIR/
cp -r resources/ $DEPLOY_DIR/

# Copier les templates s'ils existent
if [ -d "templates/" ]; then
    cp -r templates/ $DEPLOY_DIR/
fi

# Copier les fichiers de configuration
echo "⚙️ Copie des fichiers de configuration..."
cp manage.py $DEPLOY_DIR/
cp requirements.txt $DEPLOY_DIR/

# Copier les fichiers statiques buildés
echo "🎨 Copie des assets..."
cp -r staticfiles/ $DEPLOY_DIR/static/

# Créer un fichier de version
echo "📋 Création du fichier de version..."
echo "$(date '+%Y-%m-%d %H:%M:%S') - $(git rev-parse --short HEAD 2>/dev/null || echo 'no-git')" > $DEPLOY_DIR/version.txt

# 4. Upload SFTP
echo "🌐 Upload vers O2switch..."
echo "📡 Serveur: $SFTP_HOST:$SFTP_PORT"
echo "👤 Utilisateur: $SFTP_USER"

# Créer le script SFTP
cat > sftp_commands.txt << EOF
cd /
put -r $DEPLOY_DIR/* .
quit
EOF

# Exécuter l'upload SFTP
if command -v lftp >/dev/null 2>&1; then
    echo "📤 Upload avec lftp..."
    lftp -u "$SFTP_USER,$O2SWITCH_SFTP_PASSWORD" -p $SFTP_PORT $SFTP_HOST << EOF
set ftp:passive-mode on
set ftp:ssl-allow false
mirror -R $DEPLOY_DIR/ ./
quit
EOF
elif command -v sftp >/dev/null 2>&1; then
    echo "📤 Upload avec sftp..."
    echo "⚠️  Note: Vous devrez entrer le mot de passe manuellement"
    sftp -P $SFTP_PORT $SFTP_USER@$SFTP_HOST < sftp_commands.txt
else
    echo "❌ Erreur: lftp ou sftp requis pour l'upload"
    echo "💡 Installation: sudo apt install lftp"
    exit 1
fi

# 5. Nettoyage
echo "🧹 Nettoyage..."
rm -rf $DEPLOY_DIR
rm -f sftp_commands.txt

echo ""
echo "✅ Déploiement terminé avec succès !"
echo "📅 Date: $(date)"
echo "🔖 Commit: $(git rev-parse --short HEAD 2>/dev/null || echo 'no-git')"
echo "🌐 Site: https://$SFTP_HOST"