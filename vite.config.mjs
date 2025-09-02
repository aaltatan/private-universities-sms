import tailwindcss from "tailwindcss";
import { resolve } from "path";
import { defineConfig } from "vite";

export default defineConfig({
  server: {
    watch: {
      ignored: ["**/*.py", "**/*.pyc", "**/__pycache__/**"],
    },
  },
  base: "/static/",
  build: {
    manifest: "manifest.json",
    outDir: resolve("./static"),
    rollupOptions: {
      input: {
        assets: resolve("./assets/js/index.js"),
      },
    },
  },
  plugins: [],
  css: {
    postcss: {
      plugins: [tailwindcss()],
    },
  },
});
