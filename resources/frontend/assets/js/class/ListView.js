import { PageElements } from "./PageElements.js";

/**
 * constructor life cycle setting should follow instructions
 * 
 * 1. this.eleBind(): binding class attr and html element
 * 2. this.load(): loading listview data
 * 3. this.eventMount(): mount element and event
 */
export class ListView extends PageElements {
    
    listView = null

    /**
     * binding class attr and html element
     */
    eleBind() {
        this.listView = document.getElementsByClassName('list-view')[0];
    }

    /**
     * mount element and event
     */
    eventMount() {
        this.listView.addEventListener('click', async (e) => {
            // custom click event
            if (!await this.itemClick(e)) {
                return;
            }

            // list item click
            const item = e.target.closest('.list-view-item');
            if (!item || !this.listView.contains(item)) {
                return;
            }
            this.activeItem(item, !item.classList.contains('active'));
        });
    }

    /**
     * load list view datas
     */
    async load() {
        const datas = await this.datas();
        if (datas) {
            let itemsHtml = '';
            for (const data of datas) {
                itemsHtml = itemsHtml + await this.listItems(data);
            }
            itemsHtml = itemsHtml || '<h3 class="text-secondary text-center">查無資料</h3>';
            this.listView.insertAdjacentHTML('beforeend', itemsHtml);
        }
    }

    /**
     * reload list view
     */
    async reload() {
        this.listView.innerHTML = '';
        this.load();
    }

    /**
     * query or generate list view datas
     * 
     * @returns {Array}
     */
    async datas() {
        throw new Error("Please implements function queryDatas()");
    }

    /**
     * generate list item
     * 
     * @param {object} data
     * @param {string}
     * @returns {Element} list view item element
     */
    async listItems(data) {
        return `
            <div class="list-view-item">
                ${await this.itemContent(data)}
            </div>
        `;
    }

    /**
     * generate each list item content
     * 
     * @param {object} data 
     * @returns {string} element string
     */
    async itemContent(data) {
        throw new Error("Please implements function itemContent()");
    }

    /**
     * list view item custom click event
     * 
     * @param {Event} e click event
     * @returns {boolean} return true continue event action, else false
     */
    async itemClick(e) {
        return true;
    }

    /**
     * set item active
     * @param {Element} itemEle 
     * @param {boolean} isActive
     */
    activeItem(itemEle, isActive) {
        if (isActive) {
            itemEle.classList.add('active');
        } else {
            itemEle.classList.remove('active');
        }
    }
}