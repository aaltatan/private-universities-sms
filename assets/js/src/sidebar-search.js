export function sidebarSearch() {
  return {
    search: Alpine.$persist("").as("sidebar-search"),
    searchHandler() {
      let hrefs = [...document.querySelectorAll(`a[id^='sidebar-link-']`)];
      hrefs.forEach((href) => {
        let obj = {
          href: href.href,
          text: href.innerText?.toLowerCase(),
        };
        href.ariaHidden = !obj.text.includes(this.search) && !obj.href.includes(this.search);
      });
    },
  };
}