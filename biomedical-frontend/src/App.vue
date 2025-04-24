<template>
  <div>
    <nav class="bg-gray-800 p-4">
      <ul class="flex space-x-4 text-white">
        <li><router-link to="/" class="hover:underline">Home</router-link></li>
        <li><router-link to="/features" class="hover:underline">Features</router-link></li>
        <li><router-link to="/detection" class="hover:underline">Detection</router-link></li>
        <li><router-link to="/services" class="hover:underline">Services</router-link></li>
        <li><router-link to="/about" class="hover:underline">About</router-link></li>
      </ul>
    </nav>
    <router-view />
  </div>
</template>

<script setup lang="ts"></script>
