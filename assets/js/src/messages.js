export function messages(timeout, autoclose = true) {
  return {
    timer: null,
    open: true,
    close() {
      this.open = false;
    },
    init() {
      if (autoclose) {
        this.timer = setTimeout(() => this.close(), +timeout);
      }
    },
    destroy() {
      clearTimeout(this.timer);
    },
  };
}
