<template>
  <section class="py-20 bg-white">
    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">
          Works with your favorite tools
        </h2>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          Connect to 50+ popular apps and services. More integrations added every week.
        </p>
      </div>

      <!-- Integrations Grid -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
        <div
          v-for="(app, idx) in apps"
          :key="idx"
          class="group relative aspect-square bg-white rounded-2xl border-2 border-gray-200 hover:border-blue-500 hover:shadow-xl transition-all duration-300 flex items-center justify-center cursor-pointer overflow-hidden"
        >
          <!-- App Logo/Icon -->
          <div class="relative z-10 flex flex-col items-center gap-3">
            <div
              class="w-16 h-16 rounded-xl flex items-center justify-center text-2xl font-bold text-white shadow-lg"
              :style="{ background: app.gradient }"
            >
              {{ app.icon }}
            </div>
            <span class="text-sm font-semibold text-gray-700 group-hover:text-blue-600 transition-colors">
              {{ app.name }}
            </span>
          </div>

          <!-- Hover Background -->
          <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
               :style="{ background: `linear-gradient(135deg, ${app.gradient.split(',')[0].split('(')[1]} 0%, transparent 100%)` }">
          </div>

          <!-- Coming Soon Badge (if applicable) -->
          <div v-if="app.comingSoon" class="absolute top-2 right-2 px-2 py-1 bg-yellow-100 text-yellow-700 text-xs font-medium rounded-full">
            Soon
          </div>
        </div>
      </div>

      <!-- View All Link -->
      <div class="mt-12 text-center">
        <router-link
          to="/account/integrations"
          class="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-semibold group"
        >
          View all integrations
          <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
          </svg>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
const apps = [
  { name: 'Xero', icon: 'X', gradient: 'linear-gradient(135deg, #13B5EA 0%, #0E8FC7 100%)' },
  { name: 'HubSpot', icon: 'H', gradient: 'linear-gradient(135deg, #FF7A59 0%, #FF5C35 100%)' },
  { name: 'Slack', icon: 'S', gradient: 'linear-gradient(135deg, #611F69 0%, #4A154B 100%)' },
  { name: 'Jira', icon: 'J', gradient: 'linear-gradient(135deg, #2684FF 0%, #0052CC 100%)' },
  { name: 'Trello', icon: 'T', gradient: 'linear-gradient(135deg, #0079BF 0%, #026AA7 100%)' },
  { name: 'Asana', icon: 'A', gradient: 'linear-gradient(135deg, #F06A6A 0%, #E74747 100%)' },
  { name: 'Shopify', icon: 'S', gradient: 'linear-gradient(135deg, #96bf48 0%, #7ab800 100%)' },
  { name: 'Stripe', icon: 'S', gradient: 'linear-gradient(135deg, #635BFF 0%, #5144E9 100%)' },
  { name: 'Mailchimp', icon: 'M', gradient: 'linear-gradient(135deg, #FFE01B 0%, #FFC800 100%)' },
  { name: 'Zendesk', icon: 'Z', gradient: 'linear-gradient(135deg, #03363D 0%, #012329 100%)' },
  { name: 'Salesforce', icon: 'SF', gradient: 'linear-gradient(135deg, #00A1E0 0%, #0089C3 100%)' },
  { name: 'Monday', icon: 'M', gradient: 'linear-gradient(135deg, #FF3D57 0%, #E62E45 100%)' },
]
</script>
