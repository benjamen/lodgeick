<template>
  <section class="relative overflow-hidden bg-gradient-to-br from-blue-50 via-white to-purple-50 pt-32 pb-20">
    <!-- Background Pattern -->
    <div class="absolute inset-0 bg-grid-slate-100 [mask-image:linear-gradient(0deg,white,rgba(255,255,255,0.6))] -z-10"></div>

    <div class="max-w-7xl mx-auto px-6 lg:px-8">
      <div class="grid lg:grid-cols-2 gap-12 items-center">
        <!-- Left Content -->
        <div class="text-center lg:text-left">
          <div class="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium mb-6">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/>
            </svg>
            <span>One-Click Integration Platform</span>
          </div>

          <h1 class="text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            Connect Your Apps<br/>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
              In Seconds
            </span>
          </h1>

          <p class="text-xl text-gray-600 mb-8 max-w-2xl">
            Lodgeick makes integration simple. Connect your favorite tools with one click—no coding required.
            Automate workflows and sync data seamlessly.
          </p>

          <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
            <router-link
              to="/account/signup"
              class="inline-flex items-center justify-center px-8 py-4 text-base font-semibold text-white bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-200"
            >
              Get Started Free
              <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
              </svg>
            </router-link>

            <router-link
              to="/account/login"
              class="inline-flex items-center justify-center px-8 py-4 text-base font-semibold text-gray-700 bg-white border-2 border-gray-300 rounded-lg hover:border-blue-600 hover:text-blue-600 transition-all duration-200"
            >
              Log In
            </router-link>
          </div>

          <!-- Social Proof -->
          <div class="mt-12 flex items-center gap-8 justify-center lg:justify-start">
            <div class="text-center">
              <div class="text-3xl font-bold text-gray-900">50+</div>
              <div class="text-sm text-gray-600">Integrations</div>
            </div>
            <div class="w-px h-12 bg-gray-300"></div>
            <div class="text-center">
              <div class="text-3xl font-bold text-gray-900">10K+</div>
              <div class="text-sm text-gray-600">Active Users</div>
            </div>
            <div class="w-px h-12 bg-gray-300"></div>
            <div class="text-center">
              <div class="text-3xl font-bold text-gray-900">99.9%</div>
              <div class="text-sm text-gray-600">Uptime</div>
            </div>
          </div>
        </div>

        <!-- Right Content - Dashboard Preview -->
        <div class="relative">
          <div class="relative bg-white rounded-2xl shadow-2xl p-6 border border-gray-200">
            <!-- Mock Dashboard -->
            <div class="space-y-4">
              <!-- Header -->
              <div class="flex items-center justify-between pb-4 border-b border-gray-200">
                <h3 class="text-lg font-semibold text-gray-900">Your Integrations</h3>
                <span class="px-3 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">
                  Active
                </span>
              </div>

              <!-- Integration Cards -->
              <div class="space-y-3">
                <div v-for="(integration, idx) in mockIntegrations" :key="idx"
                     class="flex items-center gap-4 p-4 bg-gray-50 rounded-lg border border-gray-200 hover:border-blue-400 transition-colors">
                  <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center text-white font-bold">
                    {{ integration.icon }}
                  </div>
                  <div class="flex-1">
                    <div class="font-semibold text-gray-900">{{ integration.name }}</div>
                    <div class="text-sm text-gray-500">{{ integration.status }}</div>
                  </div>
                  <svg class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                  </svg>
                </div>
              </div>
            </div>
          </div>

          <!-- Floating Elements -->
          <div class="absolute -top-6 -right-6 w-32 h-32 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full blur-3xl opacity-30 animate-pulse"></div>
          <div class="absolute -bottom-6 -left-6 w-40 h-40 bg-gradient-to-br from-blue-400 to-cyan-400 rounded-full blur-3xl opacity-30 animate-pulse delay-1000"></div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const mockIntegrations = [
  { icon: 'X', name: 'Xero', status: 'Connected • Syncing' },
  { icon: 'H', name: 'HubSpot', status: 'Connected • Active' },
  { icon: 'S', name: 'Slack', status: 'Connected • Active' },
]
</script>

<style scoped>
.bg-grid-slate-100 {
  background-image:
    linear-gradient(to right, rgb(241 245 249 / 0.5) 1px, transparent 1px),
    linear-gradient(to bottom, rgb(241 245 249 / 0.5) 1px, transparent 1px);
  background-size: 24px 24px;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.5;
  }
}

.delay-1000 {
  animation-delay: 1s;
}
</style>
