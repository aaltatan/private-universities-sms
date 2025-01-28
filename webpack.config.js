const path = require("path");

module.exports = (env, argv) => {
  const isProduction = argv.mode === 'production';
  return {
    entry: "./assets/js/index.js",
    mode: "production",
    output: {
      path: path.resolve(__dirname, "static"),
      filename: isProduction ? "main.min.js" : "main.dev.js",
    },
  };
};
