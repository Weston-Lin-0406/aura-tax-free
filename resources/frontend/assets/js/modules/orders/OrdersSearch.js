import { PageElements } from "../../class/PageElements.js";

export class OrdersSearch extends PageElements {

    name = null;

    phone = null;

    store = null;

    dateStart = null;
    
    dateEnd = null;

    completeSwitch = null;

    submitBtn = null;

    submitFunction = null;

    /**
     * 
     * @param {Function} submitCallback 
     */
    constructor(submitCallback) {
        super();
        this.submitFunction = submitCallback;
        this.eleBind();
        this.eventMount();
    }

    /**
     * binding class attr and html element
     */
    eleBind() {
        this.name = document.getElementById('searchName');
        this.phone = document.getElementById('searchPhone');
        this.store = document.getElementById('searchStore');
        this.completeSwitch = document.getElementById('searchCompleteSwitch');
        this.dateStart = document.getElementById('searchDateStart');
        this.dateEnd = document.getElementById('searchDateEnd');
        this.submitBtn = document.getElementById('searchSubmitBtn');
    }

    /**
     * mount element and event
     */
    eventMount() {
        // search date range
        const startPick = flatpickr("#dateStart", {
            locale: "zh_tw",
            dateFormat: "Y-m-d",
            onChange: function(selectedDates) {
                if (selectedDates.length) {
                    endPick.set("minDate", selectedDates[0]);
                } else {
                    endPick.set("minDate", null);
                }
            }
        });
        const endPick = flatpickr("#dateEnd", {
            locale: "zh_tw",
            dateFormat: "Y-m-d",
            onChange: function(selectedDates) {
                if (selectedDates.length) {
                    startPick.set("maxDate", selectedDates[0]);
                } else {
                    startPick.set("maxDate", null);
                }
            }
        });
        // search submit
        this.submitBtn.addEventListener('click', () => {
            this.submitFunction();
        });
    }

    /**
     * get search params
     * 
     * @returns {object}
     */
    searchParams() {
        const params = {
            name: this.name.value,
            phone: this.phone.value,
            store: this.store.value,
            is_export: !this.completeSwitch.checked,
        }
        
        if (this.dateStart.value) {
            params.start_date = this.dateStart.value;
        }

        if (this.dateEnd.value) {
            params.end_date = this.dateEnd.value;
        }

        return params;
    }

}