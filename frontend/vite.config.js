import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The proxy forwards any request starting with /api to the Python backend,
// so the React code can just call fetch("/api/...").
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
