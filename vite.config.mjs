import tailwindcss from "@tailwindcss/vite";
import { resolve } from "path";
import { defineConfig } from "vite";

export default defineConfig({
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
  plugins: [tailwindcss()],
});
