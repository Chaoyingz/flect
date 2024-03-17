import path from "path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const serverConfig = {
  host: true,
  port: 3000,
  proxy: {
    "/flect": "http://localhost:8000/",
  },
};

const version = process.env.npm_package_version;

export default defineConfig({
  plugins: [react()],
  base: `https://unpkg.com/docs-ui@${version}/dist/`,
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: serverConfig,
  preview: serverConfig,
  build: {
    rollupOptions: {
      output: {
        entryFileNames: `assets/[name].js`,
        chunkFileNames: `assets/[name].js`,
        assetFileNames: `assets/[name].[ext]`,
      },
      plugins: [],
    },
  },
});
