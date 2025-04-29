<template>
  <div class="bg-white">
    <!-- Header -->
    <div class="relative bg-primary-700">
      <div class="absolute inset-0">
        <img class="w-full h-full object-cover" src="https://images.unsplash.com/photo-1525130413817-d45c1d127c42?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1920&q=60&&sat=-100" alt="About background" />
        <div class="absolute inset-0 bg-primary-700 mix-blend-multiply" aria-hidden="true" />
      </div>
      <div class="relative max-w-7xl mx-auto py-24 px-4 sm:py-32 sm:px-6 lg:px-8">
        <h1 class="text-4xl font-extrabold tracking-tight text-white sm:text-5xl lg:text-6xl">About BioMedVision</h1>
        <p class="mt-6 text-xl text-primary-100 max-w-3xl">
          An open-source biomedical detection platform designed for education and research in biomedical engineering.
        </p>
      </div>
    </div>

    <!-- Project description -->
    <div class="relative py-16 bg-white overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:grid lg:grid-cols-2 lg:gap-8">
          <div class="prose prose-lg text-gray-500 lg:max-w-none">
            <h2 class="text-base text-primary-600 font-semibold tracking-wide uppercase">Project Overview</h2>
            <h3 class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              Advancing Biomedical Education
            </h3>
            <p>
              BioMedVision is an open-source project created to provide biomedical engineering students and researchers with a powerful yet accessible tool for real-time biomedical detection and analysis. The platform leverages state-of-the-art computer vision models to detect and track various human features with potential biomedical applications.
            </p>
            <p>
              Originally developed as part of a portfolio project, BioMedVision has grown into a comprehensive educational resource that demonstrates the practical application of AI and computer vision in biomedical contexts.
            </p>
            <h3 class="mt-8 text-2xl leading-8 font-extrabold tracking-tight text-gray-900">
              Educational Value
            </h3>
            <p>
              This project serves multiple educational purposes:
            </p>
            <ul role="list">
              <li>Demonstrates integration of computer vision in biomedical applications</li>
              <li>Provides a complete full-stack implementation example</li>
              <li>Shows best practices in AI model deployment</li>
              <li>Offers a foundation for student projects and research</li>
            </ul>
          </div>
          <div class="mt-12 relative lg:mt-0">
            <div class="relative mx-auto max-w-md px-4 sm:max-w-3xl sm:px-6 lg:px-0">
              <div class="relative pt-64 pb-10 rounded-2xl shadow-xl overflow-hidden">
                <img class="absolute inset-0 h-full w-full object-cover" src="https://images.unsplash.com/photo-1581093450021-4a7360e9a9e1?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1000&q=80" alt="Biomedical education" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Team section -->
    <div class="bg-gray-50">
      <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8">
        <div class="lg:grid lg:grid-cols-2 lg:gap-8 lg:items-center">
          <div>
            <h2 class="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              About the Creator
            </h2>
            <p class="mt-3 max-w-3xl text-lg text-gray-500">
              Badr Ribzat is a developer with a passion for biomedical engineering applications. 
              This project was created to showcase skills in full-stack development, computer vision, 
              and AI deployment while providing value to the biomedical education community.
            </p>
            <div class="mt-8 sm:flex space-x-3">
              <div class="rounded-md shadow">
                <a href="https://github.com/BadrRibzat" target="_blank" class="flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700">
                  <svg class="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                    <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd" />
                  </svg>
                  GitHub Profile
                </a>
              </div>
              <div class="rounded-md shadow">
                <a href="https://linkedin.com/in/yourprofile" target="_blank" class="flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
                  <svg class="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                   </svg>
                  LinkedIn
                </a>
              </div>
            </div>
          </div>
          <div class="mt-8 lg:mt-0">
            <div class="flex items-center space-x-6">
              <div class="flex-shrink-0">
                <img 
                  class="h-32 w-32 rounded-full object-cover shadow-lg" 
                  src="/images/profile.jpg" 
                  alt="Badr Ribzat"
                />
              </div>
              <div class="flex-1">
                <h3 class="text-xl font-medium text-gray-900">Badr Ribzat</h3>
                <p class="text-gray-500">Full Stack Developer & Biomedical Enthusiast</p>
                <div class="mt-2 flex space-x-4">
                  <a href="mailto:your@email.com" class="text-gray-400 hover:text-gray-500">
                    <span class="sr-only">Email</span>
                    <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 12.713l-11.985-9.713h23.97l-11.985 9.713zm0 2.574l-12-9.725v15.438h24v-15.438l-12 9.725z"/>
                    </svg>
                  </a>
                  <a href="https://github.com/BadrRibzat" target="_blank" class="text-gray-400 hover:text-gray-500">
                    <span class="sr-only">GitHub</span>
                    <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                      <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd" />
                    </svg>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Open source section -->
    <div class="bg-white">
      <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8">
        <div class="lg:grid lg:grid-cols-2 lg:gap-8 lg:items-center">
          <div class="mb-8 lg:mb-0">
            <img class="w-full rounded-lg shadow-xl" src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80" alt="Open source" />
          </div>
          <div>
            <h2 class="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              Open Source Philosophy
            </h2>
            <p class="mt-3 max-w-3xl text-lg text-gray-500">
              BioMedVision is completely open-source under the MIT license. We believe in open collaboration and knowledge sharing, especially in educational contexts.
            </p>
            <div class="mt-8">
              <div class="inline-flex rounded-md shadow">
                <a href="https://github.com/BadrRibzat/biomediacl" target="_blank" class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700">
                  View on GitHub
                  <ArrowRightIcon class="ml-3 -mr-1 h-5 w-5" />
                </a>
              </div>
              <div class="ml-3 inline-flex">
                <a href="https://github.com/BadrRibzat/biomediacl/blob/master/LICENSE" target="_blank" class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-primary-700 bg-primary-100 hover:bg-primary-200">
                  MIT License
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ArrowRightIcon } from '@heroicons/vue/outline'
</script>
