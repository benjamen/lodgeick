<template>
  <div
    class="relative bg-white rounded-xl border-2 transition-all duration-300 hover:shadow-lg"
    :class="[
      isConnected
        ? 'border-green-500 bg-green-50'
        : 'border-gray-200 hover:border-blue-300',
    ]"
  >
    <!-- Connected Badge -->
    <div
      v-if="isConnected"
      class="absolute top-3 right-3 flex items-center gap-1 px-2 py-1 text-xs font-medium text-green-700 bg-green-100 rounded-full"
    >
      <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
        <path
          fill-rule="evenodd"
          d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
          clip-rule="evenodd"
        />
      </svg>
      Connected
    </div>

    <!-- Card Content -->
    <div class="p-6">
      <!-- Icon -->
      <div
        class="inline-flex items-center justify-center w-16 h-16 mb-4 text-3xl rounded-xl"
        :class="app.color"
      >
        {{ app.icon }}
      </div>

      <!-- App Name -->
      <h3 class="text-xl font-semibold text-gray-900 mb-2">
        {{ app.name }}
      </h3>

      <!-- Description -->
      <p class="text-sm text-gray-600 mb-4 h-10">
        {{ app.description }}
      </p>

      <!-- Action Button -->
      <button
        v-if="!isConnected"
        class="w-full px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors"
        @click="handleConnect"
      >
        Connect {{ app.name }}
      </button>

      <button
        v-else
        class="w-full px-4 py-2 text-sm font-medium text-gray-600 bg-gray-50 border border-gray-200 rounded-lg hover:bg-gray-100 transition-colors"
        @click="handleDisconnect"
      >
        Disconnect
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  app: {
    type: Object,
    required: true,
  },
  isConnected: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['connect', 'disconnect'])

const handleConnect = () => {
  emit('connect', props.app.id)
}

const handleDisconnect = () => {
  emit('disconnect', props.app.id)
}
</script>
