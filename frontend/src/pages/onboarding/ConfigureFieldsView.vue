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
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
      <!-- Progress Bar -->
      <StepProgressBar :current-step="onboardingStore.currentStep" :total-steps="4" />

      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          Configure Field Mappings
        </h1>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          Customize how data flows between your apps (Optional)
        </p>
      </div>

      <!-- Field Mapping Cards -->
      <div class="space-y-6 mb-8">
        <div
          v-for="integration in mockIntegrations"
          :key="integration.id"
          class="bg-white rounded-xl shadow-lg overflow-hidden"
        >
          <!-- Integration Header -->
          <div class="bg-gradient-to-r from-blue-500 to-purple-600 p-6 text-white">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-4">
                <div class="flex items-center">
                  <div class="w-12 h-12 bg-white rounded-lg flex items-center justify-center text-2xl">
                    {{ integration.fromApp.icon }}
                  </div>
                  <svg class="w-6 h-6 mx-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                  <div class="w-12 h-12 bg-white rounded-lg flex items-center justify-center text-2xl">
                    {{ integration.toApp.icon }}
                  </div>
                </div>
                <div>
                  <h3 class="text-lg font-semibold">
                    {{ integration.fromApp.name }} → {{ integration.toApp.name }}
                  </h3>
                  <p class="text-sm text-blue-100">
                    {{ integration.description }}
                  </p>
                </div>
              </div>
              <button
                class="text-white hover:text-blue-100 transition-colors"
                @click="toggleIntegration(integration.id)"
              >
                <svg
                  class="w-6 h-6 transform transition-transform"
                  :class="expandedIntegrations.includes(integration.id) ? 'rotate-180' : ''"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Field Mapping Content -->
          <div
            v-if="expandedIntegrations.includes(integration.id)"
            class="p-6"
          >
            <!-- Preset Templates -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Quick Template
              </label>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                <button
                  v-for="template in integration.templates"
                  :key="template.id"
                  class="p-3 border-2 rounded-lg text-left transition-all hover:border-blue-500 hover:bg-blue-50"
                  :class="
                    selectedTemplates[integration.id] === template.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200'
                  "
                  @click="selectTemplate(integration.id, template.id)"
                >
                  <div class="font-medium text-gray-900">{{ template.name }}</div>
                  <div class="text-sm text-gray-600">{{ template.description }}</div>
                </button>
              </div>
            </div>

            <!-- Field Mappings -->
            <div class="space-y-4">
              <div class="text-sm font-medium text-gray-700 mb-3">
                Field Mappings
              </div>
              <div
                v-for="(field, index) in integration.fields"
                :key="index"
                class="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg"
              >
                <div>
                  <label class="block text-xs font-medium text-gray-600 mb-1">
                    From {{ integration.fromApp.name }}
                  </label>
                  <select
                    v-model="field.from"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option v-for="option in field.fromOptions" :key="option" :value="option">
                      {{ option }}
                    </option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-600 mb-1">
                    To {{ integration.toApp.name }}
                  </label>
                  <select
                    v-model="field.to"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option v-for="option in field.toOptions" :key="option" :value="option">
                      {{ option }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex justify-between items-center">
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
            label="Skip for Now"
            @click="skipConfiguration"
          />

          <PrimaryButton
            label="Complete Setup"
            @click="completeOnboarding"
          >
            <template #iconRight>
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </template>
          </PrimaryButton>
        </div>
      </div>

      <!-- Help Text -->
      <div class="text-center mt-8">
        <p class="text-sm text-gray-500">
          💡 Don't worry, you can always modify these mappings later in your settings
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
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

const expandedIntegrations = ref([])
const selectedTemplates = ref({})

const mockIntegrations = computed(() => {
  const connectedApps = onboardingStore.connectedApps
    .map(id => onboardingStore.availableApps.find(app => app.id === id))
    .filter(Boolean)

  const integrations = []
  for (let i = 0; i < connectedApps.length && i < 2; i++) {
    for (let j = i + 1; j < connectedApps.length && j < 3; j++) {
      integrations.push({
        id: `${connectedApps[i].id}-${connectedApps[j].id}`,
        fromApp: connectedApps[i],
        toApp: connectedApps[j],
        description: `Sync data between ${connectedApps[i].name} and ${connectedApps[j].name}`,
        templates: [
          { id: 'default', name: 'Default', description: 'Standard field mapping' },
          { id: 'custom', name: 'Custom', description: 'Create your own mapping' },
          { id: 'advanced', name: 'Advanced', description: 'Advanced transformations' },
        ],
        fields: [
          {
            from: 'Name',
            to: 'Full Name',
            fromOptions: ['Name', 'Title', 'Description', 'Status'],
            toOptions: ['Full Name', 'Display Name', 'Label', 'State'],
          },
          {
            from: 'Email',
            to: 'Contact Email',
            fromOptions: ['Email', 'Primary Email', 'Work Email'],
            toOptions: ['Contact Email', 'Email Address', 'Primary Contact'],
          },
          {
            from: 'Phone',
            to: 'Phone Number',
            fromOptions: ['Phone', 'Mobile', 'Work Phone'],
            toOptions: ['Phone Number', 'Contact Number', 'Telephone'],
          },
        ],
      })
    }
  }

  return integrations
})

const toggleIntegration = (integrationId) => {
  const index = expandedIntegrations.value.indexOf(integrationId)
  if (index > -1) {
    expandedIntegrations.value.splice(index, 1)
  } else {
    expandedIntegrations.value.push(integrationId)
  }
}

const selectTemplate = (integrationId, templateId) => {
  selectedTemplates.value[integrationId] = templateId
}

const completeOnboarding = () => {
  // Save field mappings if needed
  Object.keys(selectedTemplates.value).forEach(integrationId => {
    onboardingStore.saveFieldMapping(integrationId, selectedTemplates.value[integrationId])
  })

  onboardingStore.completeOnboarding()
  router.push({ name: 'Dashboard' })
}

const skipConfiguration = () => {
  onboardingStore.completeOnboarding()
  router.push({ name: 'Dashboard' })
}

const goBack = () => {
  onboardingStore.previousStep()
  router.push({ name: 'Integrate' })
}
</script>
