import axios from "axios";
import { getCookie } from "./utils";

export function combobox(comboboxData = { options: [], selectedText: "" }) {
  return {
    comboboxOpen: false,
    checkAll: false,
    name: "",
    optionsConcat: "",
    textsConcat: "",
    keywords: "",
    options: comboboxData.options,
    getTitle() {
      let length = this.options.filter((e) => e.selected).length;
      return length
        ? `${length} ${comboboxData.selectedText}`
        : `${comboboxData.selectedText} ${this.name}`;
    },
    focusHandler() {
      this.$refs.comboBoxSearch?.focus();
    },
    escapeHandler() {
      this.comboboxOpen = false;
      this.keywords = "";
      this.options = this.options.map((e) => {
        e.show = true;
        return e;
      });
      this.options.sort((a, b) => b.selected - a.selected);
    },
    effectHandler() {
      this.textsConcat = this.options
        .filter((el) => el.selected)
        .map((el) => el.label)
        .join(", ");
    },
    checkAllHandler() {
      this.checkAll = !this.checkAll;
      this.options = this.options.map((e) => {
        e.selected = e.show && this.checkAll;
        return e;
      });
    },
    sortHandler() {
      this.comboboxOpen = !this.comboboxOpen;
      this.options.sort((a, b) => b.selected - a.selected);
    },
    searchHandler(el) {
      const container = el.target.closest("div[data-combo]");
      const keywords = Alpine.$data(container).keywords;

      Alpine.$data(container).options = Alpine.$data(container).options.map((e) => {
        e.show = false;
        let searchName = e.label + " " + e.label;
        let pattern = new RegExp(keywords.split(" ").join(".+"), "g");
        if (searchName.match(pattern)) {
          e.show = true;
        }
        return e;
      });
    },
    init() {
      this.name = this.$refs.comboBoxSearch.dataset.name;
      let forId = this.$el.previousElementSibling.previousElementSibling.getAttribute("for");
      this.$refs.comboBoxSearch.setAttribute("id", forId);
      let initials = location.href.match(new RegExp(`(?<=${name}\=)\d+`));
      initials = initials && initials.map((e) => +e);
      if (initials) {
        options = options.map((e) => {
          e.selected = initials.includes(e.value);
          return e;
        });
      }
    },
  };
}

export function autocomplete(data = { url, initial, eventName }) {
  return {
    keywords: "",
    isListOpen: false,
    async init() {
      if (data.initial) {
        let isNumeric = data.initial.match(/^\d+$/i);
        this.keywords = isNumeric ? await this.getInitialValue() : data.initial;
      }
    },
    openList() {
      this.isListOpen = true;
    },
    closeList() {
      this.isListOpen = false;
    },
    resetList() {
      this.$refs.list.innerHTML = "";
    },
    resetKeywords() {
      this.keywords = "";
    },
    handleSelectOption(pk) {
      this.keywords = pk;
      this.closeList();
    },
    reset() {
      this.resetKeywords();
      this.closeList();
    },
    handleRequest() {
      this.resetList();
      this.openList();
      if (this.keywords) {
        this.$dispatch(data.eventName);
      }
    },
    handleDisableInput() {
      this.$refs.input.disabled = true;
      this.$refs.indicator.classList.remove("hidden");
    },
    handleEnableInput() {
      this.$refs.input.disabled = false;
      this.$refs.indicator.classList.add("hidden");
    },
    async getInitialValue() {
      this.handleDisableInput();
      let querystring = this.$refs.input.getAttribute("querystring");
      let csrfToken = getCookie("csrftoken");
      let fullPath = `${data.url}${data.initial}/?${querystring}`;

      let response = await axios.post(fullPath, null, {
        headers: { "X-csrftoken": csrfToken },
      });
      if (response.status === 200) {
        this.handleEnableInput();
        return await response.data.value;
      } else {
        return '';
      }
    },
  };
}
