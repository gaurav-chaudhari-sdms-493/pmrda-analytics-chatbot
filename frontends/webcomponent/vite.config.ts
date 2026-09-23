import { defineConfig } from 'vite';

export default defineConfig({
  define: {
    __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
    __BUILD_VERSION__: JSON.stringify(process.env.npm_package_version || '1.0.0'),
  },
  server: {
    host: '0.0.0.0',
    port: Number(process.env.VITE_PORT) || 5174,
    proxy: {
      '/api': {
        target: process.env.VITE_BACKEND_URL || 'http://localhost:8001',
        changeOrigin: true,
        ws: true,
      },
    },
  },

  build: {
    outDir: 'dist',
    lib: {
      entry: 'src/index.ts',
      formats: ['es'],
      fileName: () => 'vanna-components.js',
    },
    rollupOptions: {
      // Remove external to bundle lit with the components
      // external: /^lit/,
    },
  },
  preview: {
    port: 9876,
    strictPort: true,
  },
});