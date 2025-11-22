import api from './utils/api.js';
import { ListView } from "./class/ListView.js";
import { Utils } from "./class/Utils.js";
import { OrdersSearch } from './modules/orders/OrdersSearch.js';
import { OrdersCreate } from './modules/orders/OrdersCreate.js';
import { OrdersEdit } from './modules/orders/OrdersEdit.js';
import { Notify } from './class/Notify.js';

export class Orders extends ListView {

    ordersList = [];

    exportOrdersBtn = null;

    unExportBtn = null;

    unExportFlag = false;

    // orders search
    ordersSearch = null;

    // orders create
    ordersCreate = null;

    // orders edit
    ordersEdit = null;

    constructor() {
        super();
        this.eleBind();
        this.load();
        this.eventMount();
    }

    /**
     * binding class attr and html element
     */
    eleBind() {
        super.eleBind();
        this.exportOrdersBtn = document.getElementById('exportOrdersBtn');
        this.unExportBtn = document.getElementById('unExportBtn');
        this.ordersSearch = new OrdersSearch(() => this.reload());
        this.ordersCreate = new OrdersCreate(() => this.reload());
        this.ordersEdit = new OrdersEdit(() => this.reload());
    }

    /**
     * mount element and event
     */
    eventMount() {
        super.eventMount();
        this.unExportBtn.addEventListener('click', () => this.selectUnExportItems());
        this.exportOrdersBtn.addEventListener('click', () => this.exportOrders());
    }

    /**
     * reload list view
     */
    async reload() {
        this.ordersList = [];
        super.reload();
    }

    /**
     * query or generate list view datas
     * 
     * @returns {Array}
     */
    async datas() {
        return await api.get('/orders/', {params: this.ordersSearch.searchParams()})
            .catch(errRes => errRes.notify());
    }

    /**
     * generate each list item content
     * 
     * @param {object} data 
     * @returns {string} element string
     */
    async itemContent(data) {
        this.ordersList.push(data);
        return `
            <div class="item-content" data-target="${data.uid}">
                <div class="d-flex justify-content-between align-items-center">
                    <div class="time mb-1">
                        <i class="fa-regular fa-calendar me-2"></i>
                        ${Utils.dateTimeFormat(data.create_time)}
                    </div>
                    <div>
                        ${this.itemCompleteBtn(data.is_export)}
                        <button class="btn btn-outline edit-item-btn">
                            <i class="fa-regular fa-pen-to-square" disabled></i>
                        </button>
                    </div>
                </div>
                <div class="primary">
                    <i class="fa-solid fa-user me-2 secondary text-dark"></i>
                    ${data.name}
                </div>
                <div class="secondary">
                    <i class="fa-solid fa-mobile-screen-button me-2"></i>
                    ${data.phone}
                </div>
                <div class="secondary">
                    <i class="fa-solid fa-shop me-1"></i>
                    ${data.store_code} ${data.store_name}
                </div>
            </div>
        `;
    }

    /**
     * list view item custom click event
     * 
     * @param {Event} e click event
     * @returns {boolean} return true continue event action, else false
     */
    async itemClick(e) {
        const ele = e.target;
        // if click item is edit btn or edit icon
        if (this.isItemEditBtn(ele) || this.isItemEditBtn(ele.parentElement)) {
            const targetUid = e.target.closest('.item-content').getAttribute('data-target');
            const orders = this.ordersList.find(orders => orders.uid == targetUid);
            this.ordersEdit.open(orders);
            return false;
        }
        return true;
    }

    /**
     * check if item is edit btn
     * 
     * @param {Element} ele 
     * @returns 
     */
    isItemEditBtn(ele) {
        return ele.classList.contains('edit-item-btn');
    }

    itemCompleteBtn(isExport) {
        return isExport ? '<button class="btn btn-sm btn-theme btn-done" disabled>已完成</button>' : '';
    }

    selectUnExportItems() {
        // active/deactive unexport items
        this.ordersList.forEach(orders => {
            if (orders.is_export) {
                return;
            }
            const item = document.querySelector(`.item-content[data-target="${orders.uid}"]`).parentElement;
            this.activeItem(item, !this.unExportFlag);
        });
        // change unExportFlag status
        if (this.unExportFlag) {
            this.unExportBtn.classList.add('btn-outline-theme');
            this.unExportBtn.classList.remove('btn-theme');
        } else {
            this.unExportBtn.classList.add('btn-theme');
            this.unExportBtn.classList.remove('btn-outline-theme');
        }
        this.unExportFlag = !this.unExportFlag;
    }

    exportOrders() {
        // get selected orders uid
        const selected = this.listView.querySelectorAll('.active .item-content');
        if (!selected || selected.length == 0) {
            Notify.show('請選擇訂單', Notify.Type.WARNING);
            return;
        }
        const uids = Array.from(selected).map(ele => ele.getAttribute('data-target'));

        // check if all selected items are done
        for (const i in this.ordersList) {
            const orders = this.ordersList[i];
            if (!uids.includes(orders.uid)) {
                continue;
            }

            if (!orders.name || !orders.phone || !orders.store_code || !orders.store_name) {
                Notify.show('尚有訂單資料未完成', Notify.Type.WARNING);
                return;
            }
        }

        // generate request params
        const params = new URLSearchParams();
        uids.forEach(uid => params.append('uids', uid));

        // export datas
        api.get('/orders/export?' + params.toString(), {
            responseType: 'blob'
        })
        .then(res => {
            // create Blob URL
            const blob = new Blob(
                [res.data],
                { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }
            );
            const url = window.URL.createObjectURL(blob);

            // download file
            const a = document.createElement('a');
            a.href = url;
            a.download = '711_shipment_orders.xlsx';
            a.click();

            // release URL
            window.URL.revokeObjectURL(url);

            // reload list view
            this.reload();
        })
        .catch(errRes => errRes.notify());
    }

}

document.addEventListener('DOMContentLoaded', () => {
    window.app = new Orders(); 
});