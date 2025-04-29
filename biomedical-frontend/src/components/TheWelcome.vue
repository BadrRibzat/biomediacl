<script setup lang="ts">
import WelcomeItem from './WelcomeItem.vue'
import DocumentationIcon from './icons/IconDocumentation.vue'
import ToolingIcon from './icons/IconTooling.vue'
import EcosystemIcon from './icons/IconEcosystem.vue'
import CommunityIcon from './icons/IconCommunity.vue'
import SupportIcon from './icons/IconSupport.vue'

const openReadmeInEditor = () => fetch('/__open-in-editor?file=README.md')
</script>

<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <WelcomeItem>
      <template #icon>
        <DocumentationIcon />
      </template>
      <template #heading>Project Documentation</template>
      Comprehensive documentation for the Biomedical Detection system is available in the
      <a 
        href="https://github.com/BadrRibzat/biomediacl/blob/master/README.md" 
        target="_blank"
        class="text-primary-600 hover:text-primary-800"
      >
        project README
      </a>.
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <ToolingIcon />
      </template>
      <template #heading>Technical Stack</template>
      This project combines:
      <ul class="list-disc pl-5 mt-2 space-y-1">
        <li><span class="font-medium">Frontend:</span> Vue 3 with TypeScript and Tailwind CSS</li>
        <li><span class="font-medium">Backend:</span> FastAPI with Python</li>
        <li><span class="font-medium">Computer Vision:</span> MediaPipe models</li>
        <li><span class="font-medium">Deployment:</span> Docker on Fly.io</li>
      </ul>
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <EcosystemIcon />
      </template>
      <template #heading>Biomedical Applications</template>
      The detection capabilities can be applied to:
      <ul class="list-disc pl-5 mt-2 space-y-1">
        <li>Physical therapy movement tracking</li>
        <li>Ergonomic posture analysis</li>
        <li>Medical education and training</li>
        <li>Assistive technology development</li>
      </ul>
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <CommunityIcon />
      </template>
      <template #heading>Open Source Community</template>
      As an open-source project, we welcome contributions from:
      <ul class="list-disc pl-5 mt-2 space-y-1">
        <li>Biomedical engineering students</li>
        <li>Computer vision researchers</li>
        <li>Full-stack developers</li>
        <li>Medical professionals</li>
      </ul>
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <SupportIcon />
      </template>
      <template #heading>Support the Project</template>
      Help improve this educational resource by:
      <ul class="list-disc pl-5 mt-2 space-y-1">
        <li>Starring the project on <a href="https://github.com/BadrRibzat/biomediacl" target="_blank" class="text-primary-600 hover:text-primary-800">GitHub</a></li>
        <li>Reporting issues or suggesting features</li>
        <li>Contributing code or documentation</li>
      </ul>
    </WelcomeItem>
  </div>
</template>

<style scoped>
a {
  transition: color 0.2s ease;
}
</style>
