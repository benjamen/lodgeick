<template>
  <section class="py-20 bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">
          How It Works
        </h2>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          Get started with Lodgeick in four simple steps
        </p>
      </div>

      <!-- Steps -->
      <div class="relative">
        <!-- Connection Line (Desktop) -->
        <div class="hidden lg:block absolute top-20 left-0 right-0 h-0.5 bg-gradient-to-r from-blue-200 via-purple-200 to-blue-200" style="width: calc(100% - 8rem); margin: 0 4rem;"></div>

        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-4">
          <div
            v-for="(step, idx) in steps"
            :key="idx"
            class="relative flex flex-col items-center text-center group"
          >
            <!-- Step Number Circle -->
            <div class="relative z-10 w-40 h-40 mb-6 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg group-hover:scale-110 group-hover:shadow-2xl transition-all duration-300">
              <div class="w-36 h-36 bg-white rounded-full flex items-center justify-center">
                <span class="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-br from-blue-500 to-purple-600">
                  {{ idx + 1 }}
                </span>
              </div>
            </div>

            <!-- Icon -->
            <div class="w-16 h-16 mb-4 bg-gradient-to-br from-blue-100 to-purple-100 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
              <component :is="step.icon" class="w-8 h-8 text-blue-600" />
            </div>

            <!-- Content -->
            <h3 class="text-xl font-bold text-gray-900 mb-3">
              {{ step.title }}
            </h3>
            <p class="text-gray-600 leading-relaxed max-w-xs">
              {{ step.description }}
            </p>
          </div>
        </div>
      </div>

      <!-- Bottom CTA -->
      <div class="mt-16 text-center">
        <router-link
          to="/account/signup"
          class="inline-flex items-center gap-2 px-8 py-4 text-base font-semibold text-white bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-200"
        >
          Start Your First Integration
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
          </svg>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
import { h } from 'vue'

const steps = [
  {
    title: 'Log In / Register',
    description: 'Create your free account in seconds. No credit card required.',
    icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' })
    ])
  },
  {
    title: 'Connect Apps',
    description: 'Choose from 50+ integrations and authorize access with one click.',
    icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z' })
    ])
  },
  {
    title: 'One-Click Integration',
    description: 'Let our system automatically configure the integration for you.',
    icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 10V3L4 14h7v7l9-11h-7z' })
    ])
  },
  {
    title: 'Optional Field Mapping',
    description: 'Customize data flow between apps with our intuitive mapping interface.',
    icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4' })
    ])
  }
]
</script>
