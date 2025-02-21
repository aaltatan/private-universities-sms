export function date() {
  return {
    formatDate(date) {
      let month = date.getMonth() + 1;
      let day = date.getDate();
      month = month.toString().padStart(2, "0");
      day = day.toString().padStart(2, "0");
      return `${date.getFullYear()}-${month}-${day}`;
    },
    insertDate(target, date) {
      if (!date) {
        date = new Date();
      }
      target.value = this.formatDate(date);
    },
    getDateFragments(value) {
      let date = new Date();
      if (value) {
        date = new Date(value);
      }
      if (isNaN(date.getTime())) {
        date = new Date();
      }
      return {
        date: date,
        year: date.getFullYear(),
        month: date.getMonth(),
        day: date.getDate(),
      };
    },
    handleDateInputDblClick(el) {
      this.insertDate(el.target);
    },
    handleDateInputFocus(el) {
      let date = new Date(el.target.value);
      if (isNaN(date.getTime()) || !el.target.value) {
        this.insertDate(el.target);
        el.target.select();
      }
    },
    handleDateInputKeyDown(el, direction) {
      let { date, day } = this.getDateFragments(el.value);
      direction === "up" ? date.setDate(day + 1) : date.setDate(day - 1);
      this.insertDate(el, date);
    },
    handleDateInputAltKeyDown(el, direction) {
      let { date, year, day } = this.getDateFragments(el.value);
      if (direction === "up") {
        date.setFullYear(year + 1);
        date.setDate(day - 1);
      } else {
        date.setFullYear(year - 1);
        date.setDate(day + 1);
      }
      this.insertDate(el, date);
    },
    handleDateInputShiftKeyDown(el, direction) {
      let { date, month, day } = this.getDateFragments(el.value);
      if (direction === "up") {
        date.setMonth(month + 1);
        date.setDate(day - 1);
      } else {
        date.setMonth(month - 1);
        date.setDate(day + 1);
      }
      this.insertDate(el, date);
    },
  };
}
