import collapse from "@alpinejs/collapse";
import focus from "@alpinejs/focus";
import mask from "@alpinejs/mask";
import persist from "@alpinejs/persist";
import sort from "@alpinejs/sort";
import Autosize from "@marcreichel/alpine-autosize";
import Alpine from "alpinejs";
import htmx from "htmx.org";
import "../css/main.css";
import "../favicon.ico";
import "../images/road.jpg";
import "../images/user.png";

window.htmx = htmx;
window.Alpine = Alpine;

import { alert } from "./src/alert";
import { badge } from "./src/badge";
import { combineTitle } from "./src/combine-title";
import { contextMenu } from "./src/context-menu";
import { autocomplete, combobox, date } from "./src/fields";
import { formset } from "./src/formset";
import { layout, sidebarLinks, theme } from "./src/layout";
import { messages } from "./src/messages";
import { tableCheckAll } from "./src/td-check-all";
import { tableTotals } from "./src/table-totals";

Alpine.plugin(collapse);
Alpine.plugin(focus);
Alpine.plugin(sort);
Alpine.plugin(persist);
Alpine.plugin(mask);
Alpine.plugin(Autosize);

document.addEventListener("alpine:init", () => {
  Alpine.data("layout", layout);
  Alpine.data("sidebarLinks", sidebarLinks);
  Alpine.data("combineTitle", combineTitle);
  Alpine.data("theme", theme);
  Alpine.data("contextMenu", contextMenu);
  Alpine.data("tableCheckAll", tableCheckAll);
  Alpine.data("alert", alert);
  Alpine.data("badge", badge);
  Alpine.data("messages", messages);
  Alpine.data("autocomplete", autocomplete);
  Alpine.data("date", date);
  Alpine.data("combobox", combobox);
  Alpine.data("formset", formset);
  Alpine.data("tableTotals", tableTotals);
});

Alpine.start();
