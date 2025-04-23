<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center justify-center">
    <h1 class="text-4xl font-bold mb-8 flex items-center text-gray-800">
      <Icon name="heroicons:camera-solid" class="w-8 h-8 mr-2 text-primary-500" />
      Test Object Detection
    </h1>
    <div class="grid grid-cols-2 gap-4">
      <UButton
        color="primary"
        size="lg"
        icon="heroicons:eye-solid"
        @click="startDetection('eyes')"
        class="shadow-md"
      >
        Test Eyes Detection
      </UButton>
      <UButton
        color="primary"
        size="lg"
        icon="heroicons:user-solid"
        @click="startDetection('head')"
        class="shadow-md"
      >
        Test Head Detection
      </UButton>
      <UButton
        color="primary"
        size="lg"
        icon="heroicons:shield-check-solid"
        @click="startDetection('arm')"
        class="shadow-md"
      >
        Test Arm Detection
      </UButton>
      <UButton
        color="primary"
        size="lg"
        icon="heroicons:hand-raised-solid"
        @click="startDetection('arm-fingers')"
        class="shadow-md"
      >
        Test Arm-Fingers Detection
      </UButton>
      <UButton
        color="primary"
        size="lg"
        icon="heroicons:users-solid"
        @click="startDetection('people')"
        class="shadow-md"
      >
        Test People Counting
      </UButton>
    </div>
    <p v-if="message" class="mt-4 text-lg text-gray-600">{{ message }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: '',
    }
  },
  methods: {
    async startDetection(type) {
      this.message = `Starting ${type} detection... (API call placeholder)`
    },
  },
  setup() {
    definePageMeta({
      title: 'Detection - Biomedical Detection Tutorial',
    })
  },
}
</script>
