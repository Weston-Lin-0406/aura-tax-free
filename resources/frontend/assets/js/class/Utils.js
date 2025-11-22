export class Utils {

    /**
     * format message
     * 1. replace \n to <br>
     * 2. add <a> at each URL
     * 
     * @param {string} text 
     * @returns 
     */
    static formatText(text) {
        let msg = text.replace(/\n/g, '<br>');
        const urls = this.extractURLs(text);
        if (urls) {
            urls.forEach(url => msg = msg.replaceAll(url, `<a href="${url}" target="_blank">${url}</a>`));
        }
        return msg;
    }

    /**
     * format date/dateTime string to yyyy - mm - dd
     * 
     * @param {string} dateString 
     * @returns 
     */
    static dateTimeFormat(dateString) {
        const dateObject = new Date(dateString);

        const year = dateObject.getFullYear();
        let month = dateObject.getMonth() + 1;
        let day = dateObject.getDate();

        // add 0
        month = String(month).padStart(2, '0');
        day = String(day).padStart(2, '0');

        return `${year}-${month}-${day}`;
    }

}
