<template>
  <div class="py-12 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="lg:text-center">
        <h2 class="text-base text-primary-600 font-semibold tracking-wide uppercase">Features</h2>
        <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
          Comprehensive Biomedical Detection
        </p>
        <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
          Our platform provides a suite of detection capabilities designed for biomedical education and research.
        </p>
      </div>

      <div class="mt-10">
        <div class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
          <div v-for="feature in features" :key="feature.title" class="relative">
            <dt>
              <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                <component :is="feature.icon" class="h-6 w-6" />
              </div>
              <p class="ml-16 text-lg leading-6 font-medium text-gray-900">{{ feature.title }}</p>
            </dt>
            <dd class="mt-2 ml-16 text-base text-gray-500">
              {{ feature.description }}
            </dd>
          </div>
        </div>
      </div>

      <!-- Technical details section -->
      <div class="mt-20">
        <h3 class="text-2xl font-bold text-gray-900 mb-6">Technical Specifications</h3>
        
        <div class="bg-gray-50 rounded-lg p-6 shadow">
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            <div v-for="spec in specifications" :key="spec.name" class="border border-gray-200 rounded-lg p-4">
              <h4 class="text-lg font-medium text-gray-900 mb-2">{{ spec.name }}</h4>
              <p class="text-gray-600">{{ spec.value }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Call to action -->
      <div class="mt-20 text-center">
        <router-link 
          to="/detection" 
          class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
        >
          Start Detection
          <ArrowRightIcon class="ml-3 -mr-1 h-5 w-5" />
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import HandRaisedIcon from '@heroicons/vue/24/outline/HandRaisedIcon'
import EyeIcon from '@heroicons/vue/24/outline/EyeIcon'
import UserIcon from '@heroicons/vue/24/outline/UserIcon'
import UsersIcon from '@heroicons/vue/24/outline/UsersIcon'
import AcademicCapIcon from '@heroicons/vue/24/outline/AcademicCapIcon'
import CodeBracketIcon from '@heroicons/vue/24/outline/CodeBracketIcon'
import ArrowRightIcon from '@heroicons/vue/24/outline/ArrowRightIcon'

const features = [
  {
    title: 'Arm & Hand Detection',
    description: 'Advanced tracking of arm positions and finger movements with real-time visualization.',
    icon: HandRaisedIcon,
    link: '/detection'
  },
  {
    title: 'Eye Detection',
    description: 'Accurate detection of eye positions using MediaPipe Face Mesh for precise analysis.',
    icon: EyeIcon,
    link: '/detection'
  },
  {
    title: 'Head & People Detection',
    description: 'Robust detection of head orientation and multiple people in a single frame.',
    icon: UsersIcon,
    link: '/detection'
  },
  {
    title: 'Educational Resource',
    description: 'Designed for students and researchers to explore biomedical vision technologies.',
    icon: AcademicCapIcon,
    link: '/about'
  },
  {
    title: 'Open Source',
    description: 'Completely open-source with MIT license for learning and customization.',
    icon: CodeBracketIcon,
    link: 'https://github.com/BadrRibzat/biomediacl'
  }
]

const specifications = [
  { name: 'Backend Framework', value: 'FastAPI (Python)' },
  { name: 'Frontend Framework', value: 'Vue 3 with TypeScript' },
  { name: 'Computer Vision', value: 'MediaPipe with custom models' },
  { name: 'Detection Models', value: 'Pose, Hands, Face Mesh, Face Detection' },
  { name: 'Deployment', value: 'Docker containers on Fly.io' },
  { name: 'License', value: 'MIT Open Source' },
]
</script>
