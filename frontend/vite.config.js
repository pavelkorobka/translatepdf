import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    hmr: {
      protocol: "ws",
      host: "localhost",
      port: 5173, // Указываем правильный порт
    }
  }
});