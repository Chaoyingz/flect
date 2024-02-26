import path from 'path'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import { baseUrl } from 'rollup-plugin-base-url'

const version = process.env.npm_package_version

const serverConfig = {
  host: true,
  port: 3000,
  proxy: {
    '/tui': 'http://localhost:8000/',
  },
}

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: serverConfig,
  preview: serverConfig,
  build: {
    rollupOptions: {
      output: {
        entryFileNames: `assets/[name]-${version}.js`,
        chunkFileNames: `assets/[name]-${version}.js`,
        assetFileNames: `assets/[name]-${version}.[ext]`,
      },
      plugins: [
        baseUrl({
          url: '/static',
        }),
      ],
    },
    outDir: '../python-tui/src/static/',
  },
})
