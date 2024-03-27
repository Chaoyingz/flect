// vite.config.ts
import path from "path";
import { defineConfig } from "file:///Users/chaoying/dev/os/flect/node_modules/.pnpm/vite@5.2.2_@types+node@20.11.30/node_modules/vite/dist/node/index.js";
import dts from "file:///Users/chaoying/dev/os/flect/node_modules/.pnpm/vite-plugin-dts@3.7.3_@types+node@20.11.30_typescript@5.4.3_vite@5.2.2/node_modules/vite-plugin-dts/dist/index.mjs";
import { libInjectCss } from "file:///Users/chaoying/dev/os/flect/node_modules/.pnpm/vite-plugin-lib-inject-css@2.0.0_vite@5.2.2/node_modules/vite-plugin-lib-inject-css/dist/index.js";
var __vite_injected_original_dirname =
  "/Users/chaoying/dev/os/flect/src/npm-flect";
var vite_config_default = defineConfig(({ mode }) => {
  return {
    plugins: [dts(), libInjectCss()],
    define: {
      "process.env.NODE_ENV": JSON.stringify(mode),
    },
    resolve: {
      alias: {
        "@": path.resolve(__vite_injected_original_dirname, "./src"),
      },
    },
    build: {
      lib: {
        entry: {
          index: path.resolve(__vite_injected_original_dirname, "src/index.ts"),
          components: path.resolve(
            __vite_injected_original_dirname,
            "src/components/index.ts",
          ),
        },
        name: "flect",
      },
      rollupOptions: {
        external: ["react", "react-dom"],
        output: {
          globals: {
            react: "React",
            "react-dom": "ReactDOM",
          },
        },
      },
    },
  };
});
export { vite_config_default as default };
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvVXNlcnMvY2hhb3lpbmcvZGV2L29zL2ZsZWN0L3NyYy9ucG0tZmxlY3RcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIi9Vc2Vycy9jaGFveWluZy9kZXYvb3MvZmxlY3Qvc3JjL25wbS1mbGVjdC92aXRlLmNvbmZpZy50c1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vVXNlcnMvY2hhb3lpbmcvZGV2L29zL2ZsZWN0L3NyYy9ucG0tZmxlY3Qvdml0ZS5jb25maWcudHNcIjtpbXBvcnQgcGF0aCBmcm9tIFwicGF0aFwiO1xuaW1wb3J0IHsgZGVmaW5lQ29uZmlnIH0gZnJvbSBcInZpdGVcIjtcbmltcG9ydCBkdHMgZnJvbSBcInZpdGUtcGx1Z2luLWR0c1wiO1xuaW1wb3J0IHsgbGliSW5qZWN0Q3NzIH0gZnJvbSBcInZpdGUtcGx1Z2luLWxpYi1pbmplY3QtY3NzXCI7XG5cbmV4cG9ydCBkZWZhdWx0IGRlZmluZUNvbmZpZygoeyBtb2RlIH0pID0+IHtcbiAgcmV0dXJuIHtcbiAgICBwbHVnaW5zOiBbZHRzKCksIGxpYkluamVjdENzcygpXSxcbiAgICBkZWZpbmU6IHtcbiAgICAgIFwicHJvY2Vzcy5lbnYuTk9ERV9FTlZcIjogSlNPTi5zdHJpbmdpZnkobW9kZSksXG4gICAgfSxcbiAgICByZXNvbHZlOiB7XG4gICAgICBhbGlhczoge1xuICAgICAgICBcIkBcIjogcGF0aC5yZXNvbHZlKF9fZGlybmFtZSwgXCIuL3NyY1wiKSxcbiAgICAgIH0sXG4gICAgfSxcbiAgICBidWlsZDoge1xuICAgICAgbGliOiB7XG4gICAgICAgIGVudHJ5OiB7XG4gICAgICAgICAgaW5kZXg6IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsIFwic3JjL2luZGV4LnRzXCIpLFxuICAgICAgICAgIGNvbXBvbmVudHM6IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsIFwic3JjL2NvbXBvbmVudHMvaW5kZXgudHNcIiksXG4gICAgICAgIH0sXG4gICAgICAgIG5hbWU6IFwiZmxlY3RcIixcbiAgICAgIH0sXG4gICAgICByb2xsdXBPcHRpb25zOiB7XG4gICAgICAgIGV4dGVybmFsOiBbXCJyZWFjdFwiLCBcInJlYWN0LWRvbVwiXSxcbiAgICAgICAgb3V0cHV0OiB7XG4gICAgICAgICAgZ2xvYmFsczoge1xuICAgICAgICAgICAgcmVhY3Q6IFwiUmVhY3RcIixcbiAgICAgICAgICAgIFwicmVhY3QtZG9tXCI6IFwiUmVhY3RET01cIixcbiAgICAgICAgICB9LFxuICAgICAgICB9LFxuICAgICAgfSxcbiAgICB9LFxuICB9O1xufSk7XG4iXSwKICAibWFwcGluZ3MiOiAiO0FBQWdULE9BQU8sVUFBVTtBQUNqVSxTQUFTLG9CQUFvQjtBQUM3QixPQUFPLFNBQVM7QUFDaEIsU0FBUyxvQkFBb0I7QUFIN0IsSUFBTSxtQ0FBbUM7QUFLekMsSUFBTyxzQkFBUSxhQUFhLENBQUMsRUFBRSxLQUFLLE1BQU07QUFDeEMsU0FBTztBQUFBLElBQ0wsU0FBUyxDQUFDLElBQUksR0FBRyxhQUFhLENBQUM7QUFBQSxJQUMvQixRQUFRO0FBQUEsTUFDTix3QkFBd0IsS0FBSyxVQUFVLElBQUk7QUFBQSxJQUM3QztBQUFBLElBQ0EsU0FBUztBQUFBLE1BQ1AsT0FBTztBQUFBLFFBQ0wsS0FBSyxLQUFLLFFBQVEsa0NBQVcsT0FBTztBQUFBLE1BQ3RDO0FBQUEsSUFDRjtBQUFBLElBQ0EsT0FBTztBQUFBLE1BQ0wsS0FBSztBQUFBLFFBQ0gsT0FBTztBQUFBLFVBQ0wsT0FBTyxLQUFLLFFBQVEsa0NBQVcsY0FBYztBQUFBLFVBQzdDLFlBQVksS0FBSyxRQUFRLGtDQUFXLHlCQUF5QjtBQUFBLFFBQy9EO0FBQUEsUUFDQSxNQUFNO0FBQUEsTUFDUjtBQUFBLE1BQ0EsZUFBZTtBQUFBLFFBQ2IsVUFBVSxDQUFDLFNBQVMsV0FBVztBQUFBLFFBQy9CLFFBQVE7QUFBQSxVQUNOLFNBQVM7QUFBQSxZQUNQLE9BQU87QUFBQSxZQUNQLGFBQWE7QUFBQSxVQUNmO0FBQUEsUUFDRjtBQUFBLE1BQ0Y7QUFBQSxJQUNGO0FBQUEsRUFDRjtBQUNGLENBQUM7IiwKICAibmFtZXMiOiBbXQp9Cg==
