import { camelToKebab } from "./utils";
import { money } from "./formats";

export function tableTotals(names = []) {
  return {
    totals: {},
    init() {
      names = names.map((total) => [camelToKebab(total), total]);

      for (let name of names) {
        let [kebabName, camelCaseName] = name;
        let tds = [...document.querySelectorAll(`[data-${kebabName}`)];

        for (let td of tds) {
          let value = +td.dataset[camelCaseName].replace(",", ".");

          if (this.totals[camelCaseName] === undefined) {
            this.totals[camelCaseName] = value;
          } else {
            this.totals[camelCaseName] += value;
          }
        }

        if (this.totals[camelCaseName]) {
          this.totals[camelCaseName] = money(this.totals[camelCaseName]);
        } else {
          this.totals[camelCaseName] = money(0);
        }
      }
    },
  };
}
