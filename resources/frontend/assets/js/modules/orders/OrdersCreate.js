import api from '../../utils/api.js';
import { PageElements } from "../../class/PageElements.js";
import { ErrorResponse } from '../../class/ErrorResponse.js';
import { Notify } from '../../class/Notify.js';

export class OrdersCreate extends PageElements {

    createDrawer = null;

    nameInput = null;

    phoneInput = null;

    storeCodeInput = null;

    storeNameInput = null;

    messageText = null;

    createForm = null;

    submitCallback = null;

    constructor(submitCallback) {
        super();
        this.submitCallback = submitCallback;
        this.eleBind();
        this.eventMount();
    }

    /**
     * binding class attr and html element
     */
    eleBind() {
        this.createDrawer = document.getElementById('createDrawer');
        this.nameInput = document.getElementById('createName');
        this.phoneInput = document.getElementById('createPhone');
        this.storeCodeInput = document.getElementById('createStoreCode');
        this.storeNameInput = document.getElementById('createStoreName');
        this.messageText = document.getElementById('createTextarea');
        this.createForm = document.getElementById('createForm');
    }

    /**
     * mount element and event
     */
    eventMount() {
        this.storeCodeInput.addEventListener('change', () => this.setStoreNameByCode());
        this.storeNameInput.addEventListener('change', () => this.setStoreCodeByName());
        this.messageText.addEventListener('change', () => this.parseMessageTextToOrders());
        this.createForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitOrders();
        });
        this.createDrawer.addEventListener('hidden.bs.offcanvas', () => {
            // reset input
            this.createForm.classList.remove('was-validated');
            this.nameInput.value = '';
            this.phoneInput.value = '';
            this.storeCodeInput.value = '';
            this.storeNameInput.value = '';
            this.messageText.value = '';
        });
    }

    setStoreNameByCode() {
        if (!this.storeCodeInput.value) {
            this.storeNameInput.value = '';
            return;
        }

        api.get(`/seven-store/name/${this.storeCodeInput.value}`)
        .then(result => this.storeNameInput.value = result)
        .catch(err => {
            if (err.status == 404) {
                Notify.show(err.detail, Notify.Type.INFO);
            } else {
                err.notify();
            }
        });
    }

    setStoreCodeByName() {
        if (!this.storeNameInput.value) {
            this.storeCodeInput.value = '';
            return;
        }

        api.get(`/seven-store/code/${this.storeNameInput.value}`)
        .then(result => this.storeCodeInput.value = result)
        .catch(err => {
            if (err.status == 404) {
                Notify.show(err.detail, Notify.Type.INFO);
            } else {
                err.notify();
            }
        });
    }

    async parseMessageTextToOrders() {
        const lines = this.messageText.value.split(/\r?\n/);
        let name = null,
            phone = null,
            storeCode = null,
            storeName = null;

        const keywords = ['姓名', '電話', '收件門市', '門市店號'];
        const pattern = /[:：]/;

        for (const line of lines) {
            for (const key of keywords) {

                if (!line.startsWith(key)) continue;

                const tmp = line.split(pattern);
                if (tmp.length <= 1) continue;

                const value = tmp[tmp.length - 1].trim();

                if (key === '姓名') {
                    name = value;
                } else if (key === '電話') {
                    phone = value.replace('-', '');
                } else if (key === '門市店號') {
                    storeCode = value;
                } else if (key === '收件門市') {
                    storeName = value;
                }
            }
        }

        // query store code if exits
        if (storeCode) {
            const sevenStoreName = await api.get(`/seven-store/${storeCode}`).catch(errRes => {});
            if (sevenStoreName) {
                storeName = sevenStoreName;
            }
        }

        this.nameInput.value = name;
        this.phoneInput.value = phone;
        this.storeCodeInput.value = storeCode;
        this.storeNameInput.value = storeName;
        this.messageText.value = '';
    }

    submitOrders() {
        if (!this.createForm.checkValidity()) {
            this.createForm.classList.add('was-validated');
            return;
        }

        // create orders
        api.post('/orders', {
            name: this.nameInput.value,
            phone: this.phoneInput.value,
            email: null,
            store_code: this.storeCodeInput.value,
            store_name: this.storeNameInput.value
        })
        .then(result => {
            Notify.show('已建立訂單', Notify.Type.SUCCESS);

            // close drawer
            bootstrap.Offcanvas.getOrCreateInstance(this.createDrawer).hide();

            // reload order list view
            this.submitCallback();
        })
        .catch(errRes => errRes.notify());
        
    }

}