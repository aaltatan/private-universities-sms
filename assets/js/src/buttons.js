export function setConfirmationTimer(element, buttonText, seconds = 3) {
  return {
    disabled: true,
    countdown: seconds,
    timeout: null,
    interval: null,
    init() {
      element.innerHTML = `${buttonText} (${this.countdown})`;
      this.interval = setInterval(() => {
        this.countdown -= 1;
        element.innerHTML = `${buttonText} (${this.countdown})`;
        if (this.countdown <= 0) {
          clearInterval(this.interval);
          element.innerHTML = buttonText;
        }
      }, 1_000);
      this.timeout = setTimeout(() => {
        this.disabled = false;
      }, seconds * 1_000);
    },
    destroy() {
      clearTimeout(this.timeout);
      clearInterval(this.interval);
    },
  };
}
