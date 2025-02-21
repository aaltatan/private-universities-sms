import collapse from "@alpinejs/collapse";
import focus from "@alpinejs/focus";
import mask from "@alpinejs/mask";
import persist from "@alpinejs/persist";
import sort from "@alpinejs/sort";
import Autosize from "@marcreichel/alpine-autosize";
import Alpine from "alpinejs";

window.htmx = require("htmx.org");
window.Alpine = Alpine;

import { alert } from "./src/alert";
import { badge } from "./src/badge";
import { contextMenu } from "./src/context-menu";
import { autocomplete, combobox, date } from "./src/fields";
import { layout, sidebarLinks, theme } from "./src/layout";
import { messages } from "./src/messages";
import { tableCheckAll } from "./src/td-check-all";

Alpine.plugin(collapse);
Alpine.plugin(focus);
Alpine.plugin(sort);
Alpine.plugin(persist);
Alpine.plugin(mask);
Alpine.plugin(Autosize);

document.addEventListener("alpine:init", () => {
  Alpine.data("layout", layout);
  Alpine.data("sidebarLinks", sidebarLinks);
  Alpine.data("theme", theme);
  Alpine.data("contextMenu", contextMenu);
  Alpine.data("tableCheckAll", tableCheckAll);
  Alpine.data("alert", alert);
  Alpine.data("badge", badge);
  Alpine.data("messages", messages);
  Alpine.data("autocomplete", autocomplete);
  Alpine.data("date", date);
  Alpine.data("combobox", combobox);
});

Alpine.start();
