<template>
  <div class="item border-b border-gray-200 pb-6 mb-6 last:border-b-0 last:pb-0 last:mb-0">
    <div class="flex">
      <div class="flex-shrink-0 mr-4">
        <div class="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
          <slot name="icon"></slot>
        </div>
      </div>
      <div class="flex-1">
        <h3 class="text-lg font-medium text-gray-900 mb-2">
          <slot name="heading"></slot>
        </h3>
        <div class="text-gray-600">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// No script needed for this component
</script>

<style scoped>
/* Remove old styles since we're using Tailwind */
</style>
