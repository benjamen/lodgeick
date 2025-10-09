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
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
      <!-- Progress Bar -->
      <StepProgressBar :current-step="onboardingStore.currentStep" :total-steps="4" />

      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          {{ integrationComplete ? 'Integration Complete!' : 'One-Click Integration' }}
        </h1>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          {{ integrationComplete
            ? 'Your apps are now connected and ready to work together'
            : 'Review and activate your integrations with a single click'
          }}
        </p>
      </div>

      <!-- Integration Status Card -->
      <div class="bg-white rounded-2xl shadow-xl p-8 mb-8">
        <!-- Success State -->
        <div v-if="integrationComplete" class="text-center">
          <!-- Success Animation -->
          <div class="inline-flex items-center justify-center w-24 h-24 mb-6 bg-green-100 rounded-full animate-bounce-slow">
            <svg class="w-12 h-12 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>

          <h2 class="text-2xl font-bold text-gray-900 mb-3">
            Successfully Integrated!
          </h2>

          <p class="text-gray-600 mb-8">
            {{ connectedAppsList }} are now seamlessly connected
          </p>

          <!-- Integration Summary -->
          <div class="bg-gray-50 rounded-lg p-6 mb-8">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
              <div>
                <div class="text-3xl font-bold text-blue-600 mb-1">
                  {{ onboardingStore.connectedApps.length }}
                </div>
                <div class="text-sm text-gray-600">Apps Connected</div>
              </div>
              <div>
                <div class="text-3xl font-bold text-purple-600 mb-1">
                  {{ selectedIntegrationCount }}
                </div>
                <div class="text-sm text-gray-600">Active Integrations</div>
              </div>
              <div>
                <div class="text-3xl font-bold text-green-600 mb-1">
                  100%
                </div>
                <div class="text-sm text-gray-600">Success Rate</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Loading/Progress State -->
        <div v-else-if="isIntegrating" class="text-center">
          <!-- Loading Spinner -->
          <div class="inline-flex items-center justify-center w-24 h-24 mb-6">
            <svg class="animate-spin h-24 w-24 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>

          <h2 class="text-2xl font-bold text-gray-900 mb-3">
            Setting Up Your Integrations
          </h2>

          <p class="text-gray-600 mb-8">
            Please wait while we configure your connections...
          </p>

          <!-- Progress Steps -->
          <div class="space-y-4">
            <div
              v-for="(step, index) in integrationSteps"
              :key="index"
              class="flex items-center gap-3 p-4 rounded-lg transition-all"
              :class="currentIntegrationStep > index ? 'bg-green-50' : currentIntegrationStep === index ? 'bg-blue-50' : 'bg-gray-50'"
            >
              <div
                class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center"
                :class="
                  currentIntegrationStep > index
                    ? 'bg-green-600'
                    : currentIntegrationStep === index
                    ? 'bg-blue-600'
                    : 'bg-gray-300'
                "
              >
                <svg v-if="currentIntegrationStep > index" class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <svg v-else-if="currentIntegrationStep === index" class="animate-spin w-5 h-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </div>
              <div class="flex-1 text-left">
                <div class="font-medium text-gray-900">{{ step.title }}</div>
                <div class="text-sm text-gray-600">{{ step.description }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Ready to Integrate State -->
        <div v-else class="text-center">
          <div class="inline-flex items-center justify-center w-24 h-24 mb-6 bg-blue-100 rounded-full">
            <svg class="w-12 h-12 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>

          <h2 class="text-2xl font-bold text-gray-900 mb-3">
            Ready to Integrate
          </h2>

          <p class="text-gray-600 mb-8">
            Click the button below to activate your integrations
          </p>

          <!-- Connected Apps Preview -->
          <div class="bg-gray-50 rounded-lg p-6 mb-8">
            <div class="flex flex-wrap justify-center gap-4">
              <div
                v-for="appId in onboardingStore.connectedApps"
                :key="appId"
                class="flex flex-col items-center"
              >
                <div
                  class="w-16 h-16 rounded-lg flex items-center justify-center text-2xl mb-2"
                  :class="getAppById(appId)?.color"
                >
                  {{ getAppById(appId)?.icon }}
                </div>
                <div class="text-sm font-medium text-gray-700">
                  {{ getAppById(appId)?.name }}
                </div>
              </div>
            </div>
          </div>

          <PrimaryButton
            label="Integrate Now"
            size="large"
            @click="startIntegration"
          >
            <template #icon>
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </template>
          </PrimaryButton>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex justify-between items-center">
        <SecondaryButton
          v-if="!integrationComplete"
          label="Back"
          @click="goBack"
        >
          <template #icon>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </template>
        </SecondaryButton>

        <div v-if="integrationComplete" class="flex gap-3 ml-auto">
          <SecondaryButton
            label="Skip Field Mapping"
            @click="skipToCompletion"
          />

          <PrimaryButton
            label="Configure Fields"
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
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { session } from '@/data/session'
import { useOnboardingStore } from '@/stores/onboarding'
import StepProgressBar from '@/components/onboarding/StepProgressBar.vue'
import PrimaryButton from '@/components/onboarding/PrimaryButton.vue'
import SecondaryButton from '@/components/onboarding/SecondaryButton.vue'

const router = useRouter()
const onboardingStore = useOnboardingStore()

const handleLogout = () => {
  session.logout.submit()
}

const isIntegrating = ref(false)
const integrationComplete = ref(false)
const currentIntegrationStep = ref(0)

const integrationSteps = [
  { title: 'Authenticating apps', description: 'Verifying credentials and permissions' },
  { title: 'Establishing connections', description: 'Creating secure communication channels' },
  { title: 'Configuring webhooks', description: 'Setting up real-time data synchronization' },
  { title: 'Testing integrations', description: 'Ensuring everything works correctly' },
]

const connectedAppsList = computed(() => {
  const apps = onboardingStore.connectedApps.map(id => getAppById(id)?.name).filter(Boolean)
  if (apps.length === 0) return ''
  if (apps.length === 1) return apps[0]
  if (apps.length === 2) return `${apps[0]} and ${apps[1]}`
  return `${apps.slice(0, -1).join(', ')}, and ${apps[apps.length - 1]}`
})

const selectedIntegrationCount = computed(() => {
  // Create default integrations between all connected apps
  const count = onboardingStore.connectedApps.length
  return count > 1 ? Math.floor((count * (count - 1)) / 2) : count
})

const getAppById = (appId) => {
  return onboardingStore.availableApps.find(app => app.id === appId)
}

const startIntegration = async () => {
  isIntegrating.value = true
  currentIntegrationStep.value = 0

  // Simulate integration process
  for (let i = 0; i < integrationSteps.length; i++) {
    currentIntegrationStep.value = i
    await new Promise(resolve => setTimeout(resolve, 1500))
  }

  // Create default integrations between all connected apps
  const connectedApps = onboardingStore.connectedApps
  for (let i = 0; i < connectedApps.length; i++) {
    for (let j = i + 1; j < connectedApps.length; j++) {
      onboardingStore.addIntegration(connectedApps[i], connectedApps[j])
    }
  }

  isIntegrating.value = false
  integrationComplete.value = true
}

const nextStep = () => {
  onboardingStore.nextStep()
  router.push({ name: 'Configure' })
}

const skipToCompletion = () => {
  onboardingStore.completeOnboarding()
  router.push({ name: 'Dashboard' })
}

const goBack = () => {
  onboardingStore.previousStep()
  router.push({ name: 'ConnectApps' })
}

onMounted(() => {
  // If no apps connected, redirect back
  if (onboardingStore.connectedApps.length === 0) {
    router.push({ name: 'ConnectApps' })
  }
})
</script>

<style scoped>
@keyframes bounce-slow {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-bounce-slow {
  animation: bounce-slow 2s infinite;
}
</style>
