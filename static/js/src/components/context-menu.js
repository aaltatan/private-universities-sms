export function contextMenu() {
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
