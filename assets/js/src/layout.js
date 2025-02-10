export function layout({ title }) {
  return {
    init() {
      document.title = title;
    },
    ...sidebar(),
    ...overlaySidebar(),
    ...modal(),
    ...fullWidthContainer(),
  };
}

export function theme() {
  return {
    dark: Alpine.$persist(true).as("dark"),
    toggleDark() {
      this.dark = !this.dark;
    },
  };
}

function fullWidthContainer() {
  return {
    fullWidthContainer: Alpine.$persist(false).as("full-width-container"),
    toggleFullWidthContainer() {
      this.fullWidthContainer = !this.fullWidthContainer;
    },
  };
}

function modal() {
  return {
    modalStatus: false,
    showModal() {
      this.modalStatus = !this.modalStatus;
      this.$refs.modal.remove();
    },
    hideModal() {
      this.modalStatus = false;
    },
  };
}

function overlaySidebar() {
  return {
    overlaySidebarOpened: false,
    openOverlaySidebar() {
      this.overlaySidebarOpened = true;
    },
    closeOverlaySidebar() {
      this.overlaySidebarOpened = false;
    },
    toggleOverlaySidebar() {
      this.overlaySidebarOpened = !this.overlaySidebarOpened;
    },
  };
}

function sidebar() {
  return {
    sidebarOpened: false,
    sidebarFixed: Alpine.$persist(true).as("sidebar-fixed"),
    sidebarSearch: Alpine.$persist("").as("sidebar-search"),
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
      let searchInput = document.getElementById("sidebar-search");
      this.showSidebar();
      searchInput.focus();
      searchInput.select();
    },
    sidebarSearchHandler() {
      let hrefs = [...document.querySelectorAll(`a[id^='sidebar-link-']`)];
      hrefs.forEach((href) => {
        let obj = {
          href: href.href,
          text: href.innerText?.toLowerCase(),
        };
        href.ariaHidden =
          !obj.text.includes(this.sidebarSearch) && !obj.href.includes(this.sidebarSearch);
      });
    },
  };
}
