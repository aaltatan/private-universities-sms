/** @type {import('tailwindcss').Config} */

const plugin = require("tailwindcss/plugin");

module.exports = {
  content: ["templates/**/*.html", "apps/**/*.html", "assets/**/*.js"],
  darkMode: "class",
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/container-queries"),
    require("tailwind-scrollbar")({ nocompatible: true }),
    plugin(function ({ addVariant }) {
      addVariant("has-checked", "&:has(input:checked)");
      addVariant("hx-request", "&.htmx-request");
      addVariant("hx-swap", "&.htmx-swapping");
      addVariant("hx-settle", "&.htmx-settling");
      addVariant("active", "&.active");
      addVariant("dark", "&:where(.dark, .dark *)");
      addVariant("tb-td", "& table td");
      addVariant("tb-th", "& table th");
    }),
  ],
};
