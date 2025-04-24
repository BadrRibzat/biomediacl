import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useDetectionStore = defineStore('detection', () => {
  const selectedFile = ref<File | null>(null)
  const results = ref<Record<string, any>>({})

  function setFile(file: File) {
    selectedFile.value = file
  }

  async function uploadImage(endpoint: string) {
    if (!selectedFile.value) {
      throw new Error('No file selected')
    }

    const formData = new FormData()
    formData.append('file', selectedFile.value)

    const response = await fetch(`https://biomedical-detection.fly.dev/detect/${endpoint}`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    results.value[endpoint] = data
    return data
  }

  return { selectedFile, results, setFile, uploadImage }
})
