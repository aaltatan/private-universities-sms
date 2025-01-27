export function tableCheckAll() {
  return {
    checkAll: false,
    selectedItems: 0,
    handleCheckAll() {
      const checkboxes = document.querySelectorAll("input[type=checkbox][id^=row-check-][checked]");
      this.selectedItems = checkboxes.length;
    },
    handleCheck(target) {
      const checkbox = target;
      if (checkbox.checked) {
        this.selectedItems++;
      } else {
        this.selectedItems--;
      }
    },
  };
}