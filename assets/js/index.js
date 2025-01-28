import Alpine from "alpinejs";
import collapse from "@alpinejs/collapse";
import focus from "@alpinejs/focus";
import sort from "@alpinejs/sort";
import persist from "@alpinejs/persist";
import mask from "@alpinejs/mask";
import Autosize from "@marcreichel/alpine-autosize";

window.htmx = require("htmx.org");
window.Alpine = Alpine;

import { layout, theme } from "./src/layout";
import { contextMenu } from "./src/context-menu";
import { tableCheckAll } from "./src/td-check-all";
import { sidebarSearch } from "./src/sidebar-search";
import { alert } from "./src/alert";
import { badge } from "./src/badge";
import { messages } from "./src/messages";
import { combobox } from "./src/combobox";

Alpine.plugin(collapse);
Alpine.plugin(focus);
Alpine.plugin(sort);
Alpine.plugin(persist);
Alpine.plugin(mask);
Alpine.plugin(Autosize);

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

Alpine.start();