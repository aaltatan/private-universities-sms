export function formset({ totalForms = 0, emptyFormId = "empty-form", tableId = "formset" }) {
  return {
    totalForms: totalForms,
    init() {
      this.sortHandler();
    },
    sortHandler() {
      this.resetOrderInputs();
      this.resetSerials();
    },
    resetSerials() {
      let serials = document.querySelectorAll(`#${tableId} td[data-header='#']`);
      serials.forEach((serial, idx) => {
        serial.innerHTML = idx + 1;
      });
    },
    resetOrderInputs() {
      let orders = document.querySelectorAll(`#${tableId} input[id$='-ORDER']`);
      orders.forEach((order, idx) => {
        order.value = idx + 1;
      });
    },
    addNewForm() {
      let emptyForm = document.getElementById(emptyFormId).cloneNode(true);
      emptyForm.classList.remove("hidden");
      emptyForm.removeAttribute("id");

      let reg = /__prefix__/g;
      emptyForm.innerHTML = emptyForm.innerHTML.replace(reg, this.totalForms);

      let autocompleteFields = emptyForm.querySelectorAll("input[x-ref='autocompleteInput']");
      autocompleteFields.forEach((field) => {
        htmx.process(field);
      });

      document.querySelector(`#${tableId} tbody[x-sort]`).appendChild(emptyForm);
      emptyForm.querySelector(`input:not([type='hidden'], select)`).focus();

      this.totalForms++;
      this.sortHandler();
    },
  };
}
