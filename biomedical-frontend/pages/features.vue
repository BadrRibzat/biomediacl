<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container mx-auto">
      <h1 class="text-4xl font-bold text-center mb-8 text-gray-800">Features</h1>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <UCard class="shadow-md">
          <template #header>
            <h2 class="text-2xl font-semibold flex items-center">
              <Icon name="heroicons:eye-solid" class="w-6 h-6 mr-2 text-primary-500" />
              Eyes Detection
            </h2>
          </template>
          <p class="text-gray-600">Detects and highlights eye landmarks in real-time using MediaPipe Face Mesh.</p>
        </UCard>
        <UCard class="shadow-md">
          <template #header>
            <h2 class="text-2xl font-semibold flex items-center">
              <Icon name="heroicons:user-solid" class="w-6 h-6 mr-2 text-primary-500" />
              Head Detection
            </h2>
          </template>
          <p class="text-gray-600">Identifies faces/heads with bounding boxes using MediaPipe Face Detection.</p>
        </UCard>
        <UCard class="shadow-md">
          <template #header>
            <h2 class="text-2xl font-semibold flex items-center">
              <Icon name="heroicons:shield-check-solid" class="w-6 h-6 mr-2 text-primary-500" />
              Arm Detection
            </h2>
          </template>
          <p class="text-gray-600">Tracks arm and upper body landmarks using MediaPipe Pose.</p>
        </UCard>
        <UCard class="shadow-md">
          <template #header>
            <h2 class="text-2xl font-semibold flex items-center">
              <Icon name="heroicons:hand-raised-solid" class="w-6 h-6 mr-2 text-primary-500" />
              Arm-Fingers Detection
            </h2>
          </template>
          <p class="text-gray-600">Detects hand and finger landmarks using MediaPipe Hands.</p>
        </UCard>
        <UCard class="shadow-md">
          <template #header>
            <h2 class="text-2xl font-semibold flex items-center">
              <Icon name="heroicons:users-solid" class="w-6 h-6 mr-2 text-primary-500" />
              People Counting
            </h2>
          </template>
          <p class="text-gray-600">Counts people passing near the camera using MediaPipe Pose.</p>
        </UCard>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  setup() {
    definePageMeta({
      title: 'Features - Biomedical Detection Tutorial',
    })
  },
}
</script>
