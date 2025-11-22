import { Notify } from "./Notify.js";

export class ErrorResponse {

    status = 500;

    detail = '系統錯誤';

    errObject = {};

    /**
     * error response psrser
     * 
     * @param {*} err 
     * @param {boolean} isNotify
     * @returns 
     */
    constructor(err, isNotify = true) {
        this.errObject = err;
        this.status = err.status;
        this.detail = err.response.data.detail;

        if (isNotify) {
            this.notify();
        }
    }

    notify() {
        Notify.show(this.detail, Notify.Type.ERROR);
    }
}