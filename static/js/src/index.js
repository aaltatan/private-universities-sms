import { layout } from "./components/layout";
import { contextMenu } from "./components/context-menu";
import { tableCheckAll } from "./components/td-check-all";
import { sidebarSearch } from "./components/sidebar-search";
import { alert } from "./components/alert";
import { badge } from "./components/badge";
import { theme } from "./components/theme";
import { messages } from "./components/messages";
import { combobox } from "./components/combobox";

document.addEventListener("alpine:init", () => {
  Alpine.data("layout", layout);
  Alpine.data("contextMenu", contextMenu);
  Alpine.data("tableCheckAll", tableCheckAll);
  Alpine.data("sidebarSearch", sidebarSearch);
  Alpine.data("alert", alert);
  Alpine.data("badge", badge);
  Alpine.data("theme", theme);
  Alpine.data("messages", messages);
  Alpine.data("combobox", combobox);
});
