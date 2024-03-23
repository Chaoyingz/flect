import path from "path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { splitVendorChunkPlugin } from "vite";

const serverConfig = {
  host: true,
  port: 3000,
  proxy: {
    "/flect": "http://localhost:8000/",
  },
  watch: {
    ignored: ["!**/node_modules/@chaoying/flect/**"],
  },
};

export default defineConfig({
  plugins: [react(), splitVendorChunkPlugin()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: serverConfig,
  optimizeDeps: {
    exclude: ["@chaoying/flect"],
  },
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
