import path from 'path'
import react from '@vitejs/plugin-react'
import { analyzer } from 'vite-bundle-analyzer'
import { defineConfig } from 'vite'

const version = process.env.npm_package_version

const serverConfig = {
  host: true,
  port: 3000,
  proxy: {
    '/tui': 'http://localhost:8000/',
  },
}

export default defineConfig({
  plugins: [react(), analyzer()],
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
    },
    outDir: '../python-tui/src/static/',
  },
})
