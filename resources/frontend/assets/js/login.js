import { ErrorResponse } from "./class/ErrorResponse.js";
import { PageElements } from "./class/PageElements.js"

export class Login extends PageElements {

    usernameInput = null;

    passwordInput = null;

    loginForm = null;

    constructor() {
        super();
        this.eleBind();
        this.eventMount();
        this.removeAssessToken();
    }

    eleBind() {
        this.usernameInput = document.getElementById('usernameInput');
        this.passwordInput = document.getElementById('passwordInput');
        this.loginForm = document.getElementById('loginForm');
    }

    eventMount() {
        this.loginForm.addEventListener('submit', (e) => this.login(e));
    }

    login(e) {
        e.preventDefault();
        if (!this.loginForm.checkValidity()) {
            this.loginForm.classList.add('was-validated');
            return;
        }

        const params = new URLSearchParams();
        params.append('grant_type', 'password');
        params.append('username', this.usernameInput.value);
        params.append('password', this.passwordInput.value);

        axios.post('/login', params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(result => {
            this.setAccessToken(result.data.access_token);
            window.location.href = '/index';
        })
        .catch(errRes => errRes.notify());
        
    }

    setAccessToken(token) {
        sessionStorage.setItem('accessToken', token);
    }

    removeAssessToken() {
        sessionStorage.removeItem('accessToken');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.app = new Login(); 
});