/// <reference types="vitest/config" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import eslint from 'vite-plugin-eslint';

// https://vitejs.dev/config/
export default defineConfig({
  base: '/',
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://server:3001',
        changeOrigin: true,
      },
    },    
  },
  preview: {
    host: '0.0.0.0',
    // assume we don't start server in dev and preview mode at the same time
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://server:3001',
        changeOrigin: true,
      },
    },    
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./src/setupTests.ts"],
  },
  plugins: [
    react(), eslint()
  ]  
})
