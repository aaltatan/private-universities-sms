const path = require("path");

module.exports = {
  entry: {
    path: path.resolve(__dirname, "static", "js", "src"),
  },
  mode: "production",
  output: {
    path: path.resolve(__dirname, "static", "js"),
    filename: "main.bundle.js",
  },
};
