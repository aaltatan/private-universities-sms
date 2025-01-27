export function alert() {
  return {
    alertIsVisible: true,
    hideAlert() {
      this.alertIsVisible = false;
    },
  };
}