<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4">Detection</h1>
    <div class="grid grid-cols-2 gap-4">
      <button @click="uploadImage('arm')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded">Detect Arm</button>
      <button @click="uploadImage('arm-fingers')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded">Detect Arm-Fingers</button>
      <button @click="uploadImage('eyes')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded">Detect Eyes</button>
      <button @click="uploadImage('head')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded">Detect Head</button>
      <button @click="uploadImage('people')" class="bg-blue-500 hover:bg-blue-700 text-white p-2 rounded">Detect People</button>
    </div>
    <input type="file" accept="image/jpeg" @change="onFileChange" class="mt-4" />
    <div v-if="result" class="mt-4">
      <h2 class="text-xl font-semibold">Result</h2>
      <pre class="bg-gray-100 p-4 rounded">{{ result }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useDetectionStore } from '../stores/detection'

const store = useDetectionStore()
const result = ref(null)
let selectedFile: File | null = null

const onFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    selectedFile = input.files[0]
    store.setFile(selectedFile)
  }
}

const uploadImage = async (endpoint: string) => {
  if (!store.selectedFile) {
    alert('Please select an image')
    return
  }

  try {
    const response = await store.uploadImage(endpoint)
    result.value = response
  } catch (error) {
    console.error('Error:', error)
    result.value = { error: 'Failed to process image' }
  }
}
</script>
