import { PageElements } from './class/PageElements.js';

export class Navbar extends PageElements {
    
    auraNavbar = null;

    constructor() {
        super();
        this.eleBind();
        this.init();
    }

    eleBind() {
        this.auraNavbar = document.getElementById('auraNavbar');
    }

    eventMount() {}

    init() {
        this.auraNavbar.classList.add('navbar', 'navbar-light', 'sticky-top', 'mb-4', 'shadow-sm');
        this.auraNavbar.innerHTML = this.navbarContent();
    }

    navbarContent() {
        return `
            <div class="container-fluid">
                <button class="btn btn-lg" type="button" data-bs-toggle="offcanvas" data-bs-target="#menuDrawer">
                    <i class="fa-solid fa-sm fa-bars-staggered"></i>
                </button>
            </div>
            <div class="offcanvas offcanvas-start bg-theme" tabindex="-1" id="menuDrawer">
                <div class="offcanvas-header">
                    <h5 class="card-title font-theme">
                        Menu
                    </h5>
                </div>
                <div class="offcanvas-body">
                    <div class="mb-4">
                        <a href="/index">
                            <h6 class="font-theme"><i class="fa-solid fa-house me-4"></i>首頁</h6>
                        </a>
                    </div>
                    <div class="mb-4">
                        <a href="/orders/index">
                            <h6 class="font-theme"><i class="fa-solid fa-clipboard-list me-4"></i>訂單管理</h6>
                        </a>
                    </div>
                    <div class="mb-4">
                        <a href="#">
                            <h6 class="font-theme"><i class="fa-solid fa-shop me-4"></i>7-11 門市</h6>
                        </a>
                    </div>
                    <div class="mb-4">
                        <a href="#">
                            <h6 class="font-theme"><i class="fa-solid fa-user-group me-4"></i>顧客清單</h6>
                        </a>
                    </div>
                    <a href="/login" id="logout">
                        <h6 class="font-theme"><i class="fa-solid fa-arrow-right-from-bracket me-4"></i>登出</h6>
                    </a>
                </div>
            </div>
        `;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.app = new Navbar(); 
});