<template>
  <button
    :type="type"
    :disabled="disabled"
    class="inline-flex items-center justify-center px-6 py-3 text-base font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
    :class="[sizeClass, fullWidth ? 'w-full' : '']"
    @click="handleClick"
  >
    <!-- Icon (left) -->
    <span v-if="$slots.icon" class="mr-2">
      <slot name="icon" />
    </span>

    <!-- Label -->
    <span>
      <slot>{{ label }}</slot>
    </span>

    <!-- Icon (right) -->
    <span v-if="$slots.iconRight" class="ml-2">
      <slot name="iconRight" />
    </span>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'button',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value),
  },
  fullWidth: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['click'])

const sizeClass = computed(() => {
  const sizes = {
    small: 'px-4 py-2 text-sm',
    medium: 'px-6 py-3 text-base',
    large: 'px-8 py-4 text-lg',
  }
  return sizes[props.size]
})

const handleClick = (event) => {
  if (!props.disabled) {
    emit('click', event)
  }
}
</script>
