<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center justify-center text-center">
    <h1 class="text-5xl font-bold mb-4 flex items-center">
      <Icon name="heroicons:eye-solid" class="w-10 h-10 mr-2 text-primary-500" />
      Biomedical Detection Tutorial
    </h1>
    <p class="text-xl mb-8 max-w-2xl text-gray-700">
      An open-source project for real-time object detection using your laptop camera, designed for biomedical engineering education.
    </p>
    <UButton
      to="/detection"
      color="primary"
      size="xl"
      icon="heroicons:arrow-right-solid"
      trailing
      class="shadow-lg"
    >
      Try Our Objects Detection
    </UButton>
  </div>
</template>

<script>
export default {
  setup() {
    definePageMeta({
      title: 'Home - Biomedical Detection Tutorial',
    })
  },
}
</script>
