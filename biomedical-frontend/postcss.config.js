export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
    // Debug plugin to confirm PostCSS is running
    'postcss-reporter': { clearReportedMessages: true },
  },
}
