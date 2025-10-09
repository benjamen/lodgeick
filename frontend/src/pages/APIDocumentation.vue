<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200 shadow-sm">
      <div class="max-w-7xl mx-auto px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <router-link to="/" class="flex items-center gap-3 group no-underline">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
              <span class="text-white font-bold text-xl">L</span>
            </div>
            <span class="text-2xl font-bold text-gray-900">Lodgeick</span>
          </router-link>

          <!-- Desktop Navigation -->
          <div class="hidden md:flex items-center gap-8">
            <router-link to="/" class="text-gray-700 hover:text-blue-600 font-medium transition-colors no-underline">Home</router-link>
            <router-link to="/pricing" class="text-gray-700 hover:text-blue-600 font-medium transition-colors no-underline">Pricing</router-link>
            <router-link to="/api" class="text-blue-600 font-medium no-underline">API</router-link>

            <router-link
              to="/auth"
              class="px-6 py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg hover:shadow-lg hover:scale-105 transition-all duration-200 no-underline"
            >
              Get Started
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <div class="container mx-auto px-4 py-16 pt-24">
      <div class="max-w-4xl mx-auto">
        <div class="text-center mb-12">
          <h1 class="text-5xl font-bold text-gray-900 mb-4">
            API Documentation
          </h1>
          <p class="text-xl text-gray-600">
            Build powerful integrations with the Lodgeick API
          </p>
        </div>

        <div class="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Getting Started</h2>
          <p class="text-gray-600 mb-4">
            The Lodgeick API allows you to programmatically manage integrations, workflows, and data synchronization.
            All API requests require authentication via API key.
          </p>

          <div class="bg-gray-100 rounded-lg p-4 mb-6">
            <p class="text-sm text-gray-600 mb-2">Base URL</p>
            <code class="text-blue-600 font-mono">https://api.lodgeick.com/v1</code>
          </div>

          <h3 class="text-xl font-semibold text-gray-900 mb-3">Authentication</h3>
          <p class="text-gray-600 mb-4">
            Include your API key in the Authorization header:
          </p>
          <div class="bg-gray-900 text-gray-100 rounded-lg p-4 overflow-x-auto mb-6">
            <pre class="text-sm"><code>curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.lodgeick.com/v1/integrations</code></pre>
          </div>
        </div>

        <div class="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Endpoints</h2>

          <div class="space-y-6">
            <div class="border-l-4 border-blue-500 pl-4">
              <div class="flex items-center gap-3 mb-2">
                <span class="px-2 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded">GET</span>
                <code class="text-gray-900 font-mono">/integrations</code>
              </div>
              <p class="text-gray-600">List all active integrations</p>
            </div>

            <div class="border-l-4 border-blue-500 pl-4">
              <div class="flex items-center gap-3 mb-2">
                <span class="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded">POST</span>
                <code class="text-gray-900 font-mono">/integrations</code>
              </div>
              <p class="text-gray-600">Create a new integration</p>
            </div>

            <div class="border-l-4 border-blue-500 pl-4">
              <div class="flex items-center gap-3 mb-2">
                <span class="px-2 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded">GET</span>
                <code class="text-gray-900 font-mono">/workflows</code>
              </div>
              <p class="text-gray-600">List all workflows</p>
            </div>

            <div class="border-l-4 border-blue-500 pl-4">
              <div class="flex items-center gap-3 mb-2">
                <span class="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded">POST</span>
                <code class="text-gray-900 font-mono">/workflows</code>
              </div>
              <p class="text-gray-600">Create a new workflow</p>
            </div>

            <div class="border-l-4 border-blue-500 pl-4">
              <div class="flex items-center gap-3 mb-2">
                <span class="px-2 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded">GET</span>
                <code class="text-gray-900 font-mono">/tasks</code>
              </div>
              <p class="text-gray-600">List task execution history</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">Example Request</h2>

          <div class="bg-gray-900 text-gray-100 rounded-lg p-4 overflow-x-auto">
            <pre class="text-sm"><code>{
  "name": "Sync Contacts",
  "source_app": "google_contacts",
  "destination_app": "mailchimp",
  "trigger": "on_create",
  "field_mappings": {
    "email": "email_address",
    "first_name": "FNAME",
    "last_name": "LNAME"
  }
}</code></pre>
          </div>
        </div>

        <div class="bg-blue-50 border border-blue-200 rounded-2xl p-8 text-center">
          <h3 class="text-2xl font-bold text-gray-900 mb-3">Need Help?</h3>
          <p class="text-gray-600 mb-6">
            Join our developer community or contact our API support team
          </p>
          <div class="flex gap-4 justify-center">
            <a
              href="mailto:api-support@lodgeick.com"
              class="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors no-underline"
            >
              Contact Support
            </a>
            <router-link
              to="/auth"
              class="px-6 py-3 bg-white text-blue-600 border-2 border-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors no-underline"
            >
              Get API Key
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <AppFooter />
  </div>
</template>

<script setup>
import AppFooter from '@/components/AppFooter.vue'
</script>
