#!/bin/bash

# Local deployment script for O2switch
# Uses the same steps as the GitHub Actions workflow

set -e

echo "🚀 Failaka deployment to O2switch"
echo "======================================"

# Configuration (to customize)
SFTP_HOST="${O2SWITCH_SFTP_HOST:-failaka.evendev.net}"
SFTP_USER="${O2SWITCH_SFTP_USERNAME:-github-deploy}"
SFTP_PORT="${O2SWITCH_SFTP_PORT:-21}"
DEPLOY_DIR="deploy-package"

# Check that environment variables are defined
if [ -z "$O2SWITCH_SFTP_PASSWORD" ]; then
    echo "❌ Error: O2SWITCH_SFTP_PASSWORD variable not defined"
    echo "💡 Export the variable: export O2SWITCH_SFTP_PASSWORD='your_password'"
    exit 1
fi

# 1. Build assets
echo "📦 Building SCSS assets..."
npm run build

# 2. Collect Django static files
echo "📂 Collecting static files..."
python manage.py collectstatic --noinput

# 3. Create deployment package
echo "📋 Creating deployment package..."
rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR

# Copy Python/Django files
echo "📁 Copying Django modules..."
cp -r authentication/ $DEPLOY_DIR/
cp -r client/ $DEPLOY_DIR/
cp -r entities/ $DEPLOY_DIR/
cp -r failaka/ $DEPLOY_DIR/

# Copier resources s'il contient des fichiers
if [ "$(ls -A resources/ 2>/dev/null)" ]; then
    echo "📦 Copie du dossier resources..."
    cp -r resources/ $DEPLOY_DIR/
fi

# Copier les templates s'ils existent au niveau racine
if [ -d "templates/" ]; then
    echo "📄 Copie des templates racine..."
    cp -r templates/ $DEPLOY_DIR/
else
    echo "ℹ️ Pas de dossier templates/ racine (templates dans les apps)"
fi

# Copier les fichiers de configuration
echo "⚙️ Copie des fichiers de configuration..."
cp manage.py $DEPLOY_DIR/
cp requirements.txt $DEPLOY_DIR/
cp package.json $DEPLOY_DIR/
cp webpack-config.js $DEPLOY_DIR/

# Copy sources (not node_modules)
echo "📁 Copying sources..."
cp -r src/ $DEPLOY_DIR/
cp -r assets/ $DEPLOY_DIR/

# Create build script for O2switch
echo "📋 Creating build script..."
cat > $DEPLOY_DIR/build-assets.sh << 'EOF'
#!/bin/bash
echo "📦 Installing npm dependencies..."
npm install --production
echo "🎨 Building assets..."
npm run build
echo "📂 Collecting static files..."
python manage.py collectstatic --noinput
echo "✅ Build complete!"
EOF
chmod +x $DEPLOY_DIR/build-assets.sh

# Create version file
echo "📋 Creating version file..."
echo "$(date '+%Y-%m-%d %H:%M:%S') - $(git rev-parse --short HEAD 2>/dev/null || echo 'no-git')" > $DEPLOY_DIR/version.txt

# 4. SFTP Upload
echo "🌐 Uploading to O2switch..."
echo "📡 Server: $SFTP_HOST:$SFTP_PORT"
echo "👤 User: $SFTP_USER"

# Create SFTP script
cat > sftp_commands.txt << EOF
cd /
put -r $DEPLOY_DIR/* .
quit
EOF

# Execute SFTP upload
if command -v lftp >/dev/null 2>&1; then
    echo "📤 Uploading with lftp..."
    lftp -u "$SFTP_USER,$O2SWITCH_SFTP_PASSWORD" -p $SFTP_PORT $SFTP_HOST << EOF
set ftp:passive-mode on
set ftp:ssl-allow false
mirror -R $DEPLOY_DIR/ ./
quit
EOF
elif command -v sftp >/dev/null 2>&1; then
    echo "📤 Uploading with sftp..."
    echo "⚠️  Note: You will need to enter the password manually"
    sftp -P $SFTP_PORT $SFTP_USER@$SFTP_HOST < sftp_commands.txt
else
    echo "❌ Error: lftp or sftp required for upload"
    echo "💡 Install: sudo apt install lftp"
    exit 1
fi

# 5. Cleanup
echo "🧹 Cleaning up..."
rm -rf $DEPLOY_DIR
rm -f sftp_commands.txt

echo ""
echo "✅ Deployment completed successfully!"
echo "📅 Date: $(date)"
echo "🔖 Commit: $(git rev-parse --short HEAD 2>/dev/null || echo 'no-git')"
echo "🌐 Site: https://$SFTP_HOST"