export function contextMenu() {
  return {
    isOpen: false,
    openedWithKeyboard: false,
    handleClose() {
      this.isOpen = false;
      this.openedWithKeyboard = false;
    },
    toggleOpen(e) {
      this.isOpen = !this.isOpen;
      this.$refs.contextmenu.classList.add("opacity-0");
      this.$nextTick(() => {
        this.calculatePositions(e);
        this.$refs.contextmenu.classList.remove("opacity-0");
      });
    },
    calculatePositions(event) {
      let contextmenuHeight = this.$refs.contextmenu.offsetHeight;
      let contextmenuWidth = this.$refs.contextmenu.offsetWidth;
      let react = event.target.getBoundingClientRect();
      let y = react.top + react.height;
      let x = react.left + react.width;

      if (window.innerHeight < y + contextmenuHeight) {
        this.$refs.contextmenu.style.top = window.innerHeight - contextmenuHeight - 8 + "px";
      } else {
        this.$refs.contextmenu.style.top = y + "px";
      }
      if (window.innerWidth < x + contextmenuWidth) {
        this.$refs.contextmenu.style.left = x - contextmenuWidth - 16 + "px";
      } else {
        this.$refs.contextmenu.style.left = x + "px";
      }
    },
    open() {
      this.isOpen = true;
    },
    openWithKeyboard() {
      this.openedWithKeyboard = true;
    },
  };
}
