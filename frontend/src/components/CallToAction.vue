<template>
  <section class="relative py-24 bg-gradient-to-br from-blue-600 via-purple-600 to-blue-700 overflow-hidden">
    <!-- Background Pattern -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute inset-0 bg-grid-white"></div>
    </div>

    <!-- Floating Shapes -->
    <div class="absolute top-10 left-10 w-64 h-64 bg-white/10 rounded-full blur-3xl animate-pulse"></div>
    <div class="absolute bottom-10 right-10 w-80 h-80 bg-purple-300/20 rounded-full blur-3xl animate-pulse delay-1000"></div>

    <div class="relative max-w-5xl mx-auto px-6 lg:px-8 text-center">
      <!-- Badge -->
      <div class="inline-flex items-center gap-2 px-4 py-2 bg-white/20 backdrop-blur-sm text-white rounded-full text-sm font-medium mb-6">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
        </svg>
        <span>No credit card required</span>
      </div>

      <!-- Headline -->
      <h2 class="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
        Start automating your<br/>
        workflows in minutes
      </h2>

      <!-- Subheadline -->
      <p class="text-xl md:text-2xl text-blue-100 mb-10 max-w-3xl mx-auto">
        Join thousands of teams who trust Lodgeick to connect their apps and streamline their processes.
      </p>

      <!-- CTA Button -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
        <router-link
          to="/account/signup"
          class="inline-flex items-center gap-3 px-10 py-5 text-lg font-bold text-blue-600 bg-white rounded-xl shadow-2xl hover:shadow-3xl hover:scale-105 transition-all duration-200"
        >
          Create Free Account
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
          </svg>
        </router-link>

        <router-link
          to="/account/login"
          class="inline-flex items-center gap-2 px-10 py-5 text-lg font-semibold text-white border-2 border-white/30 rounded-xl hover:bg-white/10 backdrop-blur-sm transition-all duration-200"
        >
          Sign In
        </router-link>
      </div>

      <!-- Trust Badges -->
      <div class="mt-16 flex flex-wrap items-center justify-center gap-8 text-white/80">
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5 text-green-300" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
          </svg>
          <span class="text-sm font-medium">Free forever plan</span>
        </div>
        <div class="w-px h-6 bg-white/30"></div>
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5 text-green-300" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
          </svg>
          <span class="text-sm font-medium">No credit card needed</span>
        </div>
        <div class="w-px h-6 bg-white/30"></div>
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5 text-green-300" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
          </svg>
          <span class="text-sm font-medium">Cancel anytime</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
.bg-grid-white {
  background-image:
    linear-gradient(to right, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 40px 40px;
}

.delay-1000 {
  animation-delay: 1s;
}
</style>
