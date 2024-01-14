import path from 'path'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

const serverConfig = {
  host: true,
  port: 3000,
  proxy: {
    '/api': 'http://localhost:8000',
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
        entryFileNames: `assets/[name].js`,
        chunkFileNames: `assets/[name].js`,
        assetFileNames: `assets/[name].[ext]`,
      },
    },
  },
})
