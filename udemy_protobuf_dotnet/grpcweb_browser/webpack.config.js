const path = require("path");

module.exports = {
  mode: "development",
  entry: "./client.js",
  output: {
    filename: "main.js",
    path: path.resolve(__dirname, "dist"),
    publicPath: "/dist/",
  },
  devServer: {
    host: "0.0.0.0",
    port: 8080,
    static: {
      directory: __dirname,
    },
    hot: true,
    liveReload: true,
    allowedHosts: "all",
    proxy: [
      {
        context: ["/groom.Groom"],
        target: "http://grpcweb_proxy:8080",
        changeOrigin: true,
      },
    ],
    watchFiles: ["./*.js", "./*.html"],
  },
};
