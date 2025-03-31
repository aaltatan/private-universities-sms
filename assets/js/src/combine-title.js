export function combineTitle(data) {
  return {
    data: data,
    title: "",
    init() {
      this.title = Object.entries(this.data)
        .map(([key, value]) => `${key}: ${value}`)
        .join("\n");
    },
  };
}
