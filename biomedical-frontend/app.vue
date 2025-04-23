<template>
  <UContainer>
    <!-- Navigation Bar -->
    <header class="bg-primary-600 text-white p-4 shadow-md">
      <nav class="flex justify-between items-center">
        <NuxtLink to="/" class="text-2xl font-bold flex items-center">
          <Icon name="heroicons:beaker-solid" class="w-6 h-6 mr-2" />
          Biomedical Detection
        </NuxtLink>
        <div class="space-x-4">
          <NuxtLink to="/" class="hover:text-gray-200">Home</NuxtLink>
          <NuxtLink to="/features" class="hover:text-gray-200">Features</NuxtLink>
          <NuxtLink to="/detection" class="hover:text-gray-200">Detection</NuxtLink>
        </div>
      </nav>
    </header>
    <!-- Page Content -->
    <main class="p-4">
      <NuxtPage />
    </main>
  </UContainer>
</template>
