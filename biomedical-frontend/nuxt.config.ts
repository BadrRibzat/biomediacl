// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: ['@nuxt/ui', '@nuxt/image', '@nuxt/icon', '@nuxt/fonts'],
  ui: {
    global: true,
    icons: ['heroicons', 'mdi'],
  },
  css: ['~/assets/css/tailwind.css'],
  tailwindcss: {
    cssPath: '~/assets/css/tailwind.css',
    configPath: 'tailwind.config.js',
    exposeConfig: false,
    injectPosition: 'first',
    viewer: true,
  },
  fonts: {
    defaults: {
      weights: [400, 700],
      styles: ['normal', 'italic'],
      subsets: ['latin'],
    },
    families: [
      { name: 'Inter', provider: 'google' },
      { name: 'Roboto', provider: 'google' },
    ],
  },
})
