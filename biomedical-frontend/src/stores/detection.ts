import { defineStore } from 'pinia'

export const useDetectionStore = defineStore('detection', {
  state: () => ({
    file: null as File | null,
  }),
  actions: {
    setFile(file: File) {
      this.file = file
    },
    async uploadImage(endpoint: string) {
      if (!this.file) {
        throw new Error('No file to upload')
      }

      const formData = new FormData()
      formData.append('file', this.file)

      const response = await fetch(`https://biomedical-detection.fly.dev/detect/${endpoint}`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json()
    },
  },
})
