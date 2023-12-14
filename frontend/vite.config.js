import { defineConfig } from 'vite'
import { fileURLToPath, URL } from "url";
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    }
  },
  server: {
    host: true,
    port: 8080,
    proxy: {
      "/api": {
        target: "http://backend:8000",
        // rewrite: (path) => path.replace(/^\/api/, ""),
      },
      "/media": {
        target: "http://backend:8000",
      },
      "/static": {
        target: "http://backend:8000",
      },
    },
  },
})
