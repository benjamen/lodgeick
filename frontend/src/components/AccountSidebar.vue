<template>
  <div class="flex flex-col h-full">
    <!-- Header -->
    <div class="p-6 border-b border-gray-200">
      <div class="flex items-center space-x-3">
        <div class="w-12 h-12 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center text-white font-bold text-lg">
          {{ userInitials }}
        </div>
        <div class="flex-1 min-w-0">
          <h2 class="text-sm font-semibold text-gray-900 truncate">{{ userName }}</h2>
          <p class="text-xs text-gray-500 truncate">{{ userEmail }}</p>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 p-4 space-y-1">
      <!-- Back to Dashboard -->
      <router-link
        to="/dashboard"
        @click="$emit('navigate')"
        class="flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200 group mb-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700"
      >
        <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        <span>Back to Dashboard</span>
      </router-link>

      <router-link
        v-for="item in navigation"
        :key="item.path"
        :to="item.path"
        @click="$emit('navigate')"
        class="flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200 group"
        :class="[
          isActive(item.path)
            ? 'bg-blue-50 text-blue-700'
            : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
        ]"
      >
        <component
          :is="item.icon"
          class="w-5 h-5 mr-3 transition-colors"
          :class="[
            isActive(item.path)
              ? 'text-blue-600'
              : 'text-gray-400 group-hover:text-gray-600'
          ]"
        />
        <span>{{ item.name }}</span>
        <svg
          v-if="isActive(item.path)"
          class="w-4 h-4 ml-auto text-blue-600"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fill-rule="evenodd"
            d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
            clip-rule="evenodd"
          />
        </svg>
      </router-link>
    </nav>

    <!-- Footer -->
    <div class="p-4 border-t border-gray-200">
      <button
        @click="handleLogout"
        class="w-full flex items-center px-4 py-3 text-sm font-medium text-red-700 hover:bg-red-50 rounded-lg transition-all duration-200 group"
      >
        <svg class="w-5 h-5 mr-3 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
        <span>Log Out</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { session } from '@/data/session'

// Icons as inline components
const UserIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>`
}

const CreditCardIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" /></svg>`
}

const PlugIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z" /></svg>`
}

const CogIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>`
}

const ShieldCheckIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>`
}

const TrashIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>`
}

defineEmits(['navigate'])

const route = useRoute()
const router = useRouter()

const navigation = [
  { name: 'Profile', path: '/account/profile', icon: UserIcon },
  { name: 'Subscription', path: '/account/subscription', icon: CreditCardIcon },
  { name: 'Integrations', path: '/account/integrations', icon: PlugIcon },
  { name: 'Settings', path: '/account/settings', icon: CogIcon },
  { name: 'Security', path: '/account/security', icon: ShieldCheckIcon },
  { name: 'Delete Account', path: '/account/delete', icon: TrashIcon },
]

const userName = computed(() => {
  return session.user_fullname || session.user || 'User'
})

const userEmail = computed(() => {
  return session.user || 'user@example.com'
})

const userInitials = computed(() => {
  const name = userName.value
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

const isActive = (path) => {
  return route.path === path || route.path.startsWith(path + '/')
}

const handleLogout = () => {
  session.logout.submit()
}
</script>
