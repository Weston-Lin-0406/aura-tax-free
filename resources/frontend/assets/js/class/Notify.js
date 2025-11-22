
export class Notify {

    static Type = Object.freeze({
        SUCCESS: 'alert-success',
        WARNING: 'alert-warning',
        INFO: 'alert-info',
        ERROR: 'alert-danger'
    });

    /**
     * show notify
     * 
     * @param {string} message 
     * @param {string} type 
     */
    static show(message, type = Utils.NotifyType.INFO) {
        const notification = document.createElement('div');
        notification.className = `alert ${type} notification`;
        notification.innerHTML = `
            <strong>${message}</strong>
            <button type="button" class="btn-close ms-2" onclick="this.parentElement.remove()" style="font-size: 12px;"></button>
        `;

        document.body.appendChild(notification);

        // 顯示通知
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        // 自動關閉
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 100);
        }, 2000);
    }

}