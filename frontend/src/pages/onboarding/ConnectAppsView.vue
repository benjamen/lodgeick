<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <!-- Header with Logo and Account Menu -->
    <div class="p-6">
      <div class="flex items-center justify-between">
        <router-link to="/" class="inline-flex items-center gap-3 group no-underline">
          <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-xl">L</span>
          </div>
          <span class="text-2xl font-bold text-gray-900">Lodgeick</span>
        </router-link>

        <!-- User Menu -->
        <div class="flex items-center gap-4">
          <router-link
            to="/account/profile"
            class="text-gray-700 hover:text-blue-600 font-medium transition-colors no-underline flex items-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            My Account
          </router-link>
          <button
            @click="handleLogout"
            class="text-gray-700 hover:text-red-600 font-medium transition-colors flex items-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Log Out
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
      <!-- Progress Bar -->
      <StepProgressBar :current-step="onboardingStore.currentStep" :total-steps="4" />

      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          Connect Your Apps
        </h1>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          Select the applications you want to integrate. You can connect more apps later.
        </p>
      </div>

      <!-- Connected Apps Summary -->
      <div v-if="onboardingStore.hasConnectedApps" class="mb-8">
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clip-rule="evenodd"
              />
            </svg>
            <span class="text-blue-800 font-medium">
              {{ onboardingStore.connectedApps.length }}
              {{ onboardingStore.connectedApps.length === 1 ? 'app' : 'apps' }} connected
            </span>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="onboardingStore.isLoadingApps" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        <div v-for="i in 6" :key="i" class="bg-white rounded-xl border-2 border-gray-200 p-6 animate-pulse">
          <div class="w-16 h-16 bg-gray-200 rounded-xl mb-4"></div>
          <div class="h-6 bg-gray-200 rounded mb-2"></div>
          <div class="h-4 bg-gray-200 rounded mb-4"></div>
          <div class="h-10 bg-gray-200 rounded"></div>
        </div>
      </div>

      <!-- Integration Cards Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        <IntegrationCard
          v-for="app in onboardingStore.availableApps"
          :key="app.id"
          :app="app"
          :is-connected="app.isConnected"
          @connect="handleConnect"
          @disconnect="handleDisconnect"
        />
      </div>

      <!-- Action Buttons -->
      <div class="flex justify-between items-center max-w-2xl mx-auto">
        <SecondaryButton
          label="Back"
          @click="goBack"
        >
          <template #icon>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </template>
        </SecondaryButton>

        <div class="flex gap-3">
          <SecondaryButton
            label="Skip"
            @click="skipStep"
          />

          <PrimaryButton
            :disabled="!onboardingStore.canContinue"
            label="Continue"
            @click="nextStep"
          >
            <template #iconRight>
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </template>
          </PrimaryButton>
        </div>
      </div>

      <!-- Help Text -->
      <div v-if="!onboardingStore.hasConnectedApps" class="text-center mt-8">
        <p class="text-sm text-gray-500">
          💡 Tip: Connect at least one app to continue to the next step
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { session } from '@/data/session'
import { useOnboardingStore } from '@/stores/onboarding'
import StepProgressBar from '@/components/onboarding/StepProgressBar.vue'
import IntegrationCard from '@/components/onboarding/IntegrationCard.vue'
import PrimaryButton from '@/components/onboarding/PrimaryButton.vue'
import SecondaryButton from '@/components/onboarding/SecondaryButton.vue'

const router = useRouter()
const onboardingStore = useOnboardingStore()

const handleLogout = () => {
  session.logout.submit()
}

// Load apps from backend on mount
onMounted(async () => {
  await onboardingStore.loadApps()
})

const handleConnect = (appId) => {
  onboardingStore.connectApp(appId)
}

const handleDisconnect = (appId) => {
  onboardingStore.disconnectApp(appId)
}

const nextStep = () => {
  if (onboardingStore.canContinue) {
    onboardingStore.nextStep()
    router.push({ name: 'Integrate' })
  }
}

const skipStep = () => {
  onboardingStore.nextStep()
  router.push({ name: 'Integrate' })
}

const goBack = () => {
  onboardingStore.previousStep()
  router.push({ name: 'Auth' })
}
</script>
