document.addEventListener("alpine:init", () => {
  Alpine.data("main", main);
  Alpine.data("contextMenu", contextMenu);
  Alpine.data("tableCheckAll", tableCheckAll);
  Alpine.data("sidebarSearch", sidebarSearch);
  Alpine.data("alert", alert);
  Alpine.data("badge", badge);
  Alpine.data("theme", theme);
  Alpine.data("messages", messages);
  Alpine.data("combobox", combobox);
});

function main({ title }) {
  return {
    init() {
      document.title = title;
    },
    /* --------------- sidebar --------------- */
    sidebarOpened: false,
    sidebarFixed: Alpine.$persist(true).as("sidebar-fixed"),
    toggleSidebarFixed() {
      this.sidebarFixed = !this.sidebarFixed;
    },
    toggleSidebar() {
      this.sidebarOpened = !this.sidebarOpened;
    },
    showSidebar() {
      this.sidebarOpened = true;
    },
    hideSidebar() {
      this.sidebarOpened = false;
    },
    sidebarSearchFocus() {
      searchInput = document.getElementById("sidebar-search");
      this.showSidebar();
      searchInput?.focus();
      searchInput?.select();
    },
    /* ----------- overlay sidebar ----------- */
    overlaySidebarOpened: false,
    openOverlaySidebar() {
      this.overlaySidebarOpened = true;
    },
    closeOverlaySidebar(e) {
      this.overlaySidebarOpened = false;
    },
    toggleOverlaySidebar() {
      this.overlaySidebarOpened = !this.overlaySidebarOpened;
    },
    /* ---------------- modal ---------------- */
    modalStatus: false,
    showModal() {
      this.modalStatus = !this.modalStatus;
      this.$refs.modal.remove();
    },
    hideModal() {
      this.modalStatus = false;
    },
    /* -------------- full width ------------- */
    fullWidthContainer: Alpine.$persist(false).as("full-width-container"),
    toggleFullWidthContainer() {
      this.fullWidthContainer = !this.fullWidthContainer;
    },
  };
}

function contextMenu() {
  return {
    isOpen: false,
    openedWithKeyboard: false,
    handleClose() {
      this.isOpen = false;
      this.openedWithKeyboard = false;
    },
    toggleOpen() {
      this.isOpen = !this.isOpen;
    },
    open() {
      this.isOpen = true;
    },
    openWithKeyboard() {
      this.openedWithKeyboard = true;
    },
  };
}

function tableCheckAll() {
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

function sidebarSearch() {
  return {
    search: Alpine.$persist("").as("sidebar-search"),
    searchHandler() {
      let hrefs = [...document.querySelectorAll(`a[id^='sidebar-link-']`)];
      hrefs.forEach((href) => {
        let obj = {
          href: href.href,
          text: href.innerText?.toLowerCase(),
        };
        href.ariaHidden = !obj.text.includes(this.search) && !obj.href.includes(this.search);
      });
    },
  };
}

function alert() {
  return {
    alertIsVisible: true,
    hideAlert() {
      this.alertIsVisible = false;
    },
  };
}

function badge(el) {
  return {
    showLabel: false,
    init() {
      let query = new URLSearchParams(location.search);
      let fields = el.dataset?.fields?.split(",");
      this.showLabel = fields?.some((field) => query.get(field));
    },
  };
}

function theme() {
  return {
    dark: Alpine.$persist(true).as("dark"),
    toggleDark() {
      this.dark = !this.dark;
    },
  };
}

function messages(timeout) {
  return {
    timer: null,
    open: true,
    close() {
      this.open = false;
    },
    init() {
      this.timer = setTimeout(() => this.close(), +timeout);
    },
    destroy() {
      clearTimeout(this.timer);
    },
  };
}

function combobox(comboboxData = { options: [], selectedText: "" }) {
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
