/** @type {import('tailwindcss').Config} */
const plugin = require("tailwindcss/plugin");

module.exports = {
  content: ["templates/**/*.html", "apps/**/*.html"],
  darkMode: "class",
  classList: [
    "underline",
    "whitespace-nowrap",
    "ms-2",
    "ms-4",
    "ms-6",
    "ms-8",
    "ms-10",
    "ms-12",
    "ms-14",
    "ms-16",
    "ms-18",
    "ms-20",
    "ms-24",
    "ms-28",
    "ms-32",
    "ms-36",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require("tailwind-scrollbar"),
    plugin(function ({ addVariant }) {
      addVariant("has-checked", ["&:has(input:checked)"]);
    }),
    // htmx variants
    plugin(function ({ addVariant }) {
      addVariant("hx-request", ["&.htmx-request"]);
    }),
    plugin(function ({ addVariant }) {
      addVariant("hx-swap", ["&.htmx-swapping"]);
    }),
    plugin(function ({ addVariant }) {
      addVariant("hx-settle", ["&.htmx-settling"]);
    }),
  ],
};
