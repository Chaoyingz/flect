# Custom Component

Custom components allow you to use your own developed React components within flect.
flect 的前端分为 flect 和 prebuilt 俩个包，其中 flect 是组件库，包含 flect 的所有组件，prebuilt 是渲染页面逻辑，他是一个 react 应用。
我们将通过自己创建 prebuilt 包来实现自定义组件
In this guide, we'll walk through the process of creating a simple badge component.

## Steps

1. 创建一个新的 React 项目，这里我们用 [vite](https://vitejs.dev/guide/) 做为项目构建工具。

   ```console
   pnpm create vite {project-name} --template react-ts
   cd {project-name}
   pnpm install
   ```

2. Add Tailwind and its configuration
   Install `tailwindcss` and its peer dependencies, then generate your `tailwind.config.js` and `postcss.config.js` files:

   ```console
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init
   ```

3. Edit tsconfig.json file
   Add the following code to the tsconfig.json file to resolve paths:

   ```json
   {
     "compilerOptions": {
       // ...
       "baseUrl": ".",
       "paths": {
         "@/*": ["./src/*"]
       }
       // ...
     }
   }
   ```

4. Update vite.config.ts
   Add the following code to the vite.config.ts so your app can resolve paths without error

   ```ts
   import path from 'path'
   import { defineConfig } from 'vite'
   import react from '@vitejs/plugin-react'
   import { baseUrl } from 'rollup-plugin-base-url'

   const serverConfig = {
     host: true,
     port: 3000,
     proxy: {
       '/flect': 'http://localhost:8000/',
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
         plugins: [
           baseUrl({
             url: '/static',
           }),
         ],
       },
     },
   })
   ```

5. Run the CLI
   Run the shadcn-ui init command to setup your project:
