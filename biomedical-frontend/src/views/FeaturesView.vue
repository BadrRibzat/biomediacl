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
          <div v-for="feature in features" :key="feature.name" class="relative">
            <dt>
              <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                <component :is="feature.icon" class="h-6 w-6" />
              </div>
              <p class="ml-16 text-lg leading-6 font-medium text-gray-900">{{ feature.name }}</p>
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
        <h3 class="text-2xl font-bold text-gray-900 mb-4">Ready to try it out?</h3>
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
import { 
  EyeIcon, 
  HandIcon, 
  UserIcon, 
  UsersIcon, 
  AcademicCapIcon, 
  CodeIcon,
  ServerIcon,
  LightningBoltIcon,
  ArrowRightIcon
} from '@heroicons/vue/outline'

const features = [
  {
    name: 'Arm & Hand Detection',
    description: 'Precisely tracks arm positions and finger movements using MediaPipe Pose and Hands models with landmark visualization.',
    icon: HandIcon,
  },
  {
    name: 'Eye Tracking',
    description: 'Detects iris positions and eye movements with high accuracy, useful for various biomedical applications.',
    icon: EyeIcon,
  },
  {
    name: 'Head & Face Analysis',
    description: 'Identifies head position and facial features with bounding boxes and key points for posture analysis.',
    icon: UserIcon,
  },
  {
    name: 'People Counting',
    description: 'Counts and tracks multiple people in the frame with pose estimation and movement tracking.',
    icon: UsersIcon,
  },
  {
    name: 'Educational Focus',
    description: 'Designed specifically for biomedical engineering students with detailed documentation and examples.',
    icon: AcademicCapIcon,
  },
  {
    name: 'Open Source',
    description: 'Completely open-source with MIT license for learning, customization, and extension.',
    icon: CodeIcon,
  },
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
