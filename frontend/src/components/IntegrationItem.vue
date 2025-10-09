<template>
  <div class="flex items-center justify-between p-4 bg-white border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
    <!-- Left: Icon + Info -->
    <div class="flex items-center space-x-4 flex-1 min-w-0">
      <!-- App Icon -->
      <div class="flex-shrink-0 w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-lg shadow-md">
        {{ appInitial }}
      </div>

      <!-- App Info -->
      <div class="flex-1 min-w-0">
        <h4 class="text-sm font-semibold text-gray-900 truncate">{{ integration.app_name }}</h4>
        <p class="text-xs text-gray-500 truncate">{{ integration.description || 'No description' }}</p>
        <div class="flex items-center mt-1 space-x-2">
          <span
            class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
            :class="statusClass"
          >
            <svg class="w-2 h-2 mr-1" fill="currentColor" viewBox="0 0 8 8">
              <circle cx="4" cy="4" r="3" />
            </svg>
            {{ statusText }}
          </span>
          <span v-if="integration.connected_at" class="text-xs text-gray-400">
            Connected {{ formatDate(integration.connected_at) }}
          </span>
        </div>
      </div>
    </div>

    <!-- Right: Actions -->
    <div class="flex items-center space-x-2 ml-4">
      <button
        v-if="integration.status === 'active'"
        @click="$emit('configure', integration)"
        class="px-3 py-1.5 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
      >
        Configure
      </button>
      <button
        @click="$emit('disconnect', integration)"
        class="px-3 py-1.5 text-xs font-medium text-red-700 bg-red-50 border border-red-200 rounded-lg hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
      >
        Disconnect
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  integration: {
    type: Object,
    required: true
  }
})

defineEmits(['disconnect', 'configure'])

const appInitial = computed(() => {
  return (props.integration.app_name || 'A')[0].toUpperCase()
})

const statusClass = computed(() => {
  const classes = {
    active: 'bg-green-100 text-green-800',
    inactive: 'bg-gray-100 text-gray-800',
    error: 'bg-red-100 text-red-800'
  }
  return classes[props.integration.status] || classes.inactive
})

const statusText = computed(() => {
  const texts = {
    active: 'Connected',
    inactive: 'Inactive',
    error: 'Error'
  }
  return texts[props.integration.status] || 'Unknown'
})

const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  const now = new Date()
  const diffDays = Math.floor((now - d) / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'today'
  if (diffDays === 1) return 'yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`
  return d.toLocaleDateString()
}
</script>
