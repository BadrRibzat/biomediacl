<template>
  <div class="relative bg-white overflow-hidden">
    <!-- Hero section -->
    <div class="pt-10 pb-20 sm:pt-16 lg:pt-8 lg:pb-14 lg:overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:grid lg:grid-cols-2 lg:gap-8">
          <div class="mt-12 sm:mt-16 lg:mt-0">
            <div class="pl-4 -mr-48 sm:pl-6 md:-mr-16 lg:px-0 lg:m-0 lg:relative lg:h-full">
              <img class="w-full rounded-xl shadow-xl ring-1 ring-black ring-opacity-5 lg:absolute lg:left-0 lg:h-full lg:w-auto lg:max-w-none" src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80" alt="Biomedical analysis">
            </div>
          </div>
          <div class="mt-20 lg:mt-0">
            <div class="max-w-md mx-auto lg:max-w-lg">
              <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                <span class="block">Advanced Biomedical</span>
                <span class="block text-primary-600">Detection System</span>
              </h1>
              <p class="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                An open-source platform for real-time biomedical analysis using computer vision and AI. Designed for education and research in biomedical engineering.
              </p>
              <div class="mt-10 sm:flex sm:justify-center lg:justify-start">
                <div class="rounded-md shadow">
                  <router-link to="/detection" class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 md:py-4 md:text-lg md:px-10">
                    Try Live Demo
                  </router-link>
                </div>
                <div class="mt-3 rounded-md shadow sm:mt-0 sm:ml-3">
                  <a href="https://github.com/BadrRibzat/biomediacl" target="_blank" class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-primary-600 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10">
                    View on GitHub
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features overview -->
    <div class="bg-gray-50 pt-16 pb-20 px-4 sm:px-6 lg:pt-24 lg:pb-28 lg:px-8">
      <div class="relative max-w-lg mx-auto divide-y-2 divide-gray-200 lg:max-w-7xl">
        <div>
          <h2 class="text-3xl tracking-tight font-extrabold text-gray-900 sm:text-4xl">
            Key Features
          </h2>
          <p class="mt-3 text-xl text-gray-500 sm:mt-4">
            Comprehensive biomedical detection capabilities powered by MediaPipe and AI.
          </p>
        </div>
        <div class="mt-12 grid gap-16 pt-12 lg:grid-cols-3 lg:gap-x-5 lg:gap-y-12">
          <div v-for="feature in features" :key="feature.title" class="bg-white p-6 rounded-lg shadow-lg">
            <div>
              <span class="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                <component :is="feature.icon" class="h-6 w-6" />
              </span>
            </div>
            <div class="mt-6">
              <h3 class="text-lg font-medium text-gray-900">{{ feature.title }}</h3>
              <p class="mt-2 text-base text-gray-500">
                {{ feature.description }}
              </p>
            </div>
            <div class="mt-6">
              <router-link :to="feature.link" class="text-base font-medium text-primary-600 hover:text-primary-500">
                Learn more<span aria-hidden="true"> &rarr;</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Call to action -->
    <div class="bg-primary-700">
      <div class="max-w-2xl mx-auto text-center py-16 px-4 sm:py-20 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-extrabold text-white sm:text-4xl">
          <span class="block">Ready to explore?</span>
          <span class="block">Start detecting biomedical features today.</span>
        </h2>
        <p class="mt-4 text-lg leading-6 text-primary-200">
          This open-source project is designed for students, researchers, and educators in biomedical engineering.
        </p>
        <router-link to="/detection" class="mt-8 w-full inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-primary-600 bg-white hover:bg-primary-50 sm:w-auto">
          Get Started
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
  AcademicCapIcon 
} from '@heroicons/vue/24/outline'

const features = [
  {
    title: 'Arm & Hand Detection',
    description: 'Track arm positions and finger movements with high precision using MediaPipe Pose and Hands models.',
    icon: HandIcon,
    link: '/detection'
  },
  {
    title: 'Eye Tracking',
    description: 'Detect iris positions and eye movements for potential biomedical applications like fatigue detection.',
    icon: EyeIcon,
    link: '/detection'
  },
  {
    title: 'Head & Face Analysis',
    description: 'Identify head position and facial features for posture analysis and other medical applications.',
    icon: UserIcon,
    link: '/detection'
  },
  {
    title: 'People Counting',
    description: 'Count and track multiple people in the frame with pose estimation capabilities.',
    icon: UsersIcon,
    link: '/detection'
  },
  {
    title: 'Educational Focus',
    description: 'Designed specifically for biomedical engineering students and educators.',
    icon: AcademicCapIcon,
    link: '/about'
  },
  {
    title: 'Open Source',
    description: 'Completely open-source with MIT license for learning and customization.',
    icon: 'svg',
    link: 'https://github.com/BadrRibzat/biomediacl'
  }
]
</script>
