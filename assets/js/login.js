import { Modal } from 'bootstrap';

document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');
    const togglePassword = document.getElementById('togglePassword');
    const passwordField = document.getElementById('password');

    // Gestion du formulaire de login
    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Empêche le rechargement de la page

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/api/auth/token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                const tokens = await response.json();
                // Stocker les jetons dans le localStorage ou les cookies
                localStorage.setItem('access_token', tokens.access);
                localStorage.setItem('refresh_token', tokens.refresh);

                // Fermer la popup
                const loginModal = Modal.getInstance(document.getElementById('loginModal'));
                loginModal.hide();

                // Rediriger ou mettre à jour l'interface utilisateur
                // alert('Login successful!');
                location.reload(); // Recharge la page pour refléter l'état connecté
            } else {
                loginError.classList.remove('d-none'); // Affiche un message d'erreur
            }
        } catch (error) {
            console.error('Error during login:', error);
            loginError.classList.remove('d-none');
        }
    });

    // Gestion du bouton "Afficher le mot de passe"
    togglePassword.addEventListener('click', function () {
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        this.querySelector('i').classList.toggle('bi-eye');
        this.querySelector('i').classList.toggle('bi-eye-slash');
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
        document.getElementById('loginButton').classList.add('d-none');
        document.getElementById('logoutButton').classList.remove('d-none');
    }

    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }
});

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    location.reload(); // Recharge la page après la déconnexion
}