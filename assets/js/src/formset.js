export function formset({ totalForms = 0, emptyFormId = "empty-form", tableId = "formset" }) {
  return {
    totalForms: totalForms,
    init() {
      this.resetSerials();
    },
    resetSerials() {
      let serials = document.querySelectorAll(`#${tableId} td[data-header='#']`);
      serials.forEach((serial, idx) => {
        serial.innerHTML = idx + 1;
      });
    },
    addNewForm() {
      let emptyForm = document.getElementById(emptyFormId).cloneNode(true);
      emptyForm.classList.remove("hidden");
      emptyForm.removeAttribute("id");

      let reg = /__prefix__/g;
      emptyForm.innerHTML = emptyForm.innerHTML.replace(reg, this.totalForms);

      document.querySelector(`#${tableId} tbody[x-sort]`).appendChild(emptyForm);
      emptyForm.querySelector(`input:not([type='hidden'], select)`).focus();

      this.totalForms++;
      this.resetSerials();
    },
    sortHandler() {
      let orders = document.querySelectorAll("input[id$='-ORDER']");
      orders.forEach((order, idx) => {
        if (order.value) {
          order.value = idx + 1;
        }
      });
    },
  };
}
