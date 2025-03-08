export function formset({ totalForms = 0, emptyFormId = "empty-form" }) {
  return {
    totalForms: totalForms,
    addNewForm() {
      let emptyForm = document.getElementById(emptyFormId).cloneNode(true);
      emptyForm.classList.remove("hidden");
      emptyForm.removeAttribute("id");

      let reg = /__prefix__/g;
      emptyForm.innerHTML = emptyForm.innerHTML.replace(reg, this.totalForms);

      document.querySelector("tbody").appendChild(emptyForm);
      emptyForm.querySelector(`input:not([type='hidden'], select)`).focus();

      this.totalForms++;
    },
  };
}
