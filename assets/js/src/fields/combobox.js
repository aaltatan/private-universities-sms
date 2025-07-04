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
    unCheckAllHandler() {
      this.options = this.options.map((e) => {
        e.selected = false;
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
        let searchName = e.label.toLowerCase() + " " + e.label.toLowerCase();
        let pattern = new RegExp(keywords.toLowerCase().split(" ").join(".+"), "g");
        if (searchName.match(pattern)) {
          e.show = true;
        }
        return e;
      });
    },
    init() {
      this.name = this.$refs.comboBoxSearch.dataset.name;
      let forId = this.$el.parentElement.querySelector("label").getAttribute("for");
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
