export function autocomplete(data = { url, initial, eventName, inputId }) {
  return {
    keywords: "",
    title: "",
    isListOpen: false,
    async init() {
      if (data.initial) {
        this.keywords = data.initial;
        this.title = data.initial;
      }
    },
    openList() {
      this.isListOpen = true;
    },
    closeList() {
      this.isListOpen = false;
    },
    resetList() {
      this.$refs.autocompleteList.innerHTML = "";
    },
    selectInput() {
      let input = document.getElementById(data.inputId);
      input.focus();
      input.select();
    },
    handleSelectOption(pk) {
      this.keywords = pk;
      this.title = pk;
      this.closeList();
    },
    handleCloseAndSelect() {
      this.closeList();
      this.selectInput();
    },
    onOpenAutocompleteList() {
      this.openList();
    },
    handleRequest() {
      this.closeList();
      if (this.keywords) {
        this.$dispatch(data.eventName);
      }
    },
    handleDisableInput() {
      this.$refs.autocompleteInput.disabled = true;
      this.$refs.autocompleteIndicator.classList.remove("hidden");
    },
    handleEnableInput() {
      this.$refs.autocompleteInput.disabled = false;
      this.$refs.autocompleteIndicator.classList.add("hidden");
    },
  };
}
