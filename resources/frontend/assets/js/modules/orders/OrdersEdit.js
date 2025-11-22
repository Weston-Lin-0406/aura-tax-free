import api from '../../utils/api.js';
import { PageElements } from "../../class/PageElements.js";
import { ErrorResponse } from '../../class/ErrorResponse.js';
import { Notify } from '../../class/Notify.js';

export class OrdersEdit extends PageElements {

    editDrawer = null;

    editForm = null;

    submitCallback = null;

    uidInput = null;

    nameInput = null;

    phoneInput = null;

    storeCodeInput = null;

    storeNameInput = null;

    completeSwitch = null;

    completeSwitchLabel = null;

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
        this.editDrawer = document.getElementById('editDrawer');
        this.editForm = document.getElementById('editForm');
        this.uidInput = document.getElementById('editUid');
        this.nameInput = document.getElementById('editName');
        this.phoneInput = document.getElementById('editPhone');
        this.storeCodeInput = document.getElementById('editStoreCode');
        this.storeNameInput = document.getElementById('editStoreName');
        this.completeSwitch = document.getElementById('editCompleteSwitch');
        this.completeSwitchLabel = this.completeSwitch.nextElementSibling;
    }

    /**
     * mount element and event
     */
    eventMount() {
        this.storeCodeInput.addEventListener('change', () => this.setStoreNameByCode());
        this.completeSwitch.addEventListener('change', () => {
            this.completeSwitchLabel.innerHTML = this.completeSwitch.checked ? '已完成' : '未完成';
        });
        this.editForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitOrders();
        });
        this.editDrawer.addEventListener('hidden.bs.offcanvas', () => {
            // reset input
            this.editForm.classList.remove('was-validated');
            this.uidInput.value = '';
            this.nameInput.value = '';
            this.phoneInput.value = '';
            this.storeCodeInput.value = '';
            this.storeNameInput.value = '';
        });
    }

    open(orders) {
        this.uidInput.value = orders.uid;
        this.nameInput.value = orders.name;
        this.phoneInput.value = orders.phone;
        this.storeCodeInput.value = orders.store_code;
        this.storeNameInput.value = orders.store_name;
        this.completeSwitch.checked = orders.is_export;
        this.completeSwitch.dispatchEvent(new Event("change"));
        bootstrap.Offcanvas.getOrCreateInstance(this.editDrawer).show();
    }

    setStoreNameByCode() {
        if (!this.storeCodeInput.value) {
            this.storeNameInput.value = '';
            return;
        }

        api.get(`/seven-store/${this.storeCodeInput.value}`)
        .then(result => this.storeNameInput.value = result)
        .catch(errRes => {
            if (errRes.status == 404) {
                Notify.show(errRes.detail, Notify.Type.INFO);
            } else {
                errRes.notify();
            }
        });
    }

    submitOrders() {
        if (!this.editForm.checkValidity()) {
            this.editForm.classList.add('was-validated');
            return;
        }

        // edit orders
        api.put(`/orders/${this.uidInput.value}`, {
            name: this.nameInput.value,
            phone: this.phoneInput.value,
            email: null,
            store_code: this.storeCodeInput.value,
            store_name: this.storeNameInput.value,
            is_export: this.completeSwitch.checked
        })
        .then(result => {
            Notify.show('已更新訂單', Notify.Type.SUCCESS);

            // close drawer
            bootstrap.Offcanvas.getOrCreateInstance(this.editDrawer).hide();

            // reload order list view
            this.submitCallback();
        })
        .catch(errRes => errRes.notify());
        
    }

}