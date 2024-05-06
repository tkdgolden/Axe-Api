import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
 base: "/",
 plugins: [react()],
 preview: {
  strictPort: true,
 },
 server: {
  strictPort: true,
  host: true,
  port: 3000
//   origin: "http://127.0.0.1:5173",
 },
});