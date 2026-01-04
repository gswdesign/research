import react from '@vitejs/plugin-react'
import vike from 'vike/plugin'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    react(),
    vike({
      prerender: true
    })
  ],
  server: {
    port: 3000,
    host: true
  },
  build: {
    target: 'es2022'
  }
})
