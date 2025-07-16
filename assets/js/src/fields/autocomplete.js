import { getCookie } from "../utils";

export function autocomplete(data = { url, initial, eventName }) {
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
    resetKeywords() {
      this.keywords = "";
    },
    selectInput() {
      this.$refs.autocompleteInput.select();
    },
    handleNoResults() {
      this.selectInput();
    },
    handleSelectOption(pk) {
      this.keywords = pk;
      this.title = pk;
      this.closeList();
    },
    reset() {
      this.resetKeywords();
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
    async getInitialValue() {
      this.handleDisableInput();
      let querystring = this.$refs.autocompleteInput.getAttribute("querystring");
      let csrfToken = getCookie("csrftoken");
      let fullPath = `${data.url}${data.initial}/?${querystring}`;

      let response = await fetch(fullPath, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
      });

      if (response.status === 200) {
        this.handleEnableInput();
        let data = await response.json();
        return data.value;
      } else {
        return "";
      }
    },
  };
}
