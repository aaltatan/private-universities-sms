/** @type {import('tailwindcss').Config} */
const plugin = require("tailwindcss/plugin");

module.exports = {
  content: [
    "templates/**/*.html",
    "apps/**/*.html",
  ],
  darkMode: 'class',
  classList: [
    'underline',
    'whitespace-nowrap',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('tailwind-scrollbar'),
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
}

