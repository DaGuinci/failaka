// Point d'entrée principal pour Failaka
// ====================================

// 1. Import des styles SCSS (compilation via Webpack)
import '../../src/scss/main.scss';

// 2. Import de jQuery et Bootstrap JS
import './jquery';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-table/dist/bootstrap-table.min.js';

// 3. Import des scripts spécifiques
import './login'; // Import du script de login

// 4. Initialisation globale
document.addEventListener('DOMContentLoaded', function() {
    console.log('Failaka app initialized');
});