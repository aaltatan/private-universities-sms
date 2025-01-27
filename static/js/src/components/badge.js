export function badge(el) {
  return {
    showLabel: false,
    init() {
      let query = new URLSearchParams(location.search);
      let fields = el.dataset?.fields?.split(",");
      this.showLabel = fields?.some((field) => query.get(field));
    },
  };
}