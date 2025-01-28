export function messages(timeout) {
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