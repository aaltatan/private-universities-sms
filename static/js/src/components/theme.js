export function theme() {
  return {
    dark: Alpine.$persist(true).as("dark"),
    toggleDark() {
      this.dark = !this.dark;
    },
  };
}
