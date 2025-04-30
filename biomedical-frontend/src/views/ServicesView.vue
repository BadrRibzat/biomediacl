<template>
  <div class="bg-white py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center">
        <h2 class="text-base font-semibold text-primary-600 tracking-wide uppercase">Services</h2>
        <p class="mt-2 text-3xl font-extrabold text-gray-900 sm:text-4xl">
          Biomedical Detection API Services
        </p>
        <p class="mt-3 max-w-2xl mx-auto text-xl text-gray-500 sm:mt-4">
          Our backend provides robust, real-time detection capabilities for biomedical applications.
        </p>
      </div>

      <div class="mt-12">
        <div class="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          <div v-for="service in services" :key="service.name" class="pt-6">
            <div class="flow-root bg-gray-50 rounded-lg px-6 pb-8 h-full">
              <div class="-mt-6">
                <div>
                  <span class="inline-flex items-center justify-center p-3 bg-primary-500 rounded-md shadow-lg">
                    <component :is="service.icon" class="h-6 w-6 text-white" />
                  </span>
                </div>
                <h3 class="mt-8 text-lg font-medium text-gray-900 tracking-tight">{{ service.name }}</h3>
                <p class="mt-5 text-base text-gray-500">
                  {{ service.description }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- API Documentation Section -->
      <div class="mt-20 bg-gray-50 rounded-xl p-8">
        <div class="lg:grid lg:grid-cols-2 lg:gap-8">
          <div class="mb-8 lg:mb-0">
            <h3 class="text-2xl font-bold text-gray-900 mb-4">API Documentation</h3>
            <p class="text-lg text-gray-600 mb-6">
              Our FastAPI backend provides well-documented endpoints for all detection features.
            </p>
            <div class="bg-white rounded-lg shadow p-6">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-primary-500 rounded-md p-2">
                  <CodeBracketIcon class="h-6 w-6 text-white" />
                </div>
                <div class="ml-4">
                  <h4 class="text-lg font-medium text-gray-900">Swagger UI</h4>
                  <p class="text-gray-500">Interactive API documentation</p>
                </div>
              </div>
              <div class="mt-6">
                <a 
                  href="https://biomedical-detection.fly.dev/docs" 
                  target="_blank"
                  class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
                >
                  View API Docs
                  <ArrowRightIcon class="ml-2 -mr-1 h-5 w-5" />
                </a>
              </div>
            </div>
          </div>
          <div>
            <h3 class="text-2xl font-bold text-gray-900 mb-4">Example API Request</h3>
            <div class="bg-gray-800 rounded-lg overflow-hidden">
              <pre class="p-4 text-sm text-gray-100 overflow-x-auto">
<code class="language-javascript">// Detect arm landmarks
const detectArm = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await fetch(
    'https://biomedical-detection.fly.dev/detect/arm',
    {
      method: 'POST',
      body: formData
    }
  );
  
  return await response.json();
};</code></pre>
            </div>
          </div>
        </div>
      </div>

      <!-- Deployment Section -->
      <div class="mt-20">
        <div class="lg:grid lg:grid-cols-2 lg:gap-8 lg:items-center">
          <div class="mb-8 lg:mb-0">
            <img class="w-full rounded-lg shadow-xl" src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80" alt="Deployment" />
          </div>
          <div>
            <h3 class="text-2xl font-bold text-gray-900 mb-4">Scalable Deployment</h3>
            <p class="text-lg text-gray-600 mb-6">
              Our backend is deployed on Fly.io using Docker containers for maximum scalability and reliability.
            </p>
            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div class="bg-white rounded-lg shadow p-4">
                <div class="flex items-center">
                  <ServerIcon class="h-6 w-6 text-primary-500" />
                  <h4 class="ml-3 text-lg font-medium text-gray-900">Fly.io</h4>
                </div>
                <p class="mt-2 text-gray-600">Global edge deployment</p>
              </div>
              <div class="bg-white rounded-lg shadow p-4">
                <div class="flex items-center">
                  <CubeIcon class="h-6 w-6 text-primary-500" />
                  <h4 class="ml-3 text-lg font-medium text-gray-900">Docker</h4>
                </div>
                <p class="mt-2 text-gray-600">Containerized deployment</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import ShieldCheckIcon from '@heroicons/vue/24/outline/ShieldCheckIcon';
import BoltIcon from '@heroicons/vue/24/outline/BoltIcon';
import ScaleIcon from '@heroicons/vue/24/outline/ScaleIcon';
import CodeBracketIcon from '@heroicons/vue/24/outline/CodeBracketIcon';
import ServerIcon from '@heroicons/vue/24/outline/ServerIcon';
import CubeIcon from '@heroicons/vue/24/outline/CubeIcon';
import ArrowRightIcon from '@heroicons/vue/24/outline/ArrowRightIcon';

const services = [
  {
    name: 'Secure Processing',
    description: 'All image processing is done securely on our servers with no client-side data storage.',
    icon: ShieldCheckIcon,
  },
  {
    name: 'High-Performance Models',
    description: 'Utilizing optimized MediaPipe models for real-time detection with low latency.',
    icon: BoltIcon,
  },
  {
    name: 'Scalable Infrastructure',
    description: 'Designed to scale automatically based on demand with Docker containers on Fly.io.',
    icon: ScaleIcon,
  },
]
</script>

<style scoped>
pre code {
  font-family: 'Fira Code', monospace;
  line-height: 1.5;
}
</style>
