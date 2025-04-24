import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    port: 5173,
  },
  optimizeDeps: {
    exclude: [
      '@mediapipe/pose',
      '@mediapipe/hands',
      '@mediapipe/face_mesh',
      '@mediapipe/face_detection'
    ]
  },
  build: {
    rollupOptions: {
      external: [
        '@mediapipe/pose',
        '@mediapipe/hands',
        '@mediapipe/face_mesh',
        '@mediapipe/face_detection'
      ]
    }
  }
})
