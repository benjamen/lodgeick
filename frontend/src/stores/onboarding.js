import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useOnboardingStore = defineStore('onboarding', () => {
  // State
  const currentStep = ref(1)
  const totalSteps = ref(4)
  const isCompleted = ref(false)
  const connectedApps = ref([])
  const selectedIntegrations = ref([])
  const fieldMappings = ref({})

  // Available apps for integration
  const availableApps = ref([
    {
      id: 'jira',
      name: 'Jira',
      description: 'Project management and issue tracking',
      icon: '🎯',
      color: 'bg-blue-500',
      isConnected: false,
    },
    {
      id: 'slack',
      name: 'Slack',
      description: 'Team communication and collaboration',
      icon: '💬',
      color: 'bg-purple-500',
      isConnected: false,
    },
    {
      id: 'hubspot',
      name: 'HubSpot',
      description: 'CRM and marketing automation',
      icon: '🎨',
      color: 'bg-orange-500',
      isConnected: false,
    },
    {
      id: 'google_sheets',
      name: 'Google Sheets',
      description: 'Spreadsheets and data management',
      icon: '📊',
      color: 'bg-green-500',
      isConnected: false,
    },
    {
      id: 'salesforce',
      name: 'Salesforce',
      description: 'Customer relationship management',
      icon: '☁️',
      color: 'bg-blue-600',
      isConnected: false,
    },
    {
      id: 'mailchimp',
      name: 'Mailchimp',
      description: 'Email marketing platform',
      icon: '✉️',
      color: 'bg-yellow-500',
      isConnected: false,
    },
  ])

  // Computed
  const progress = computed(() => (currentStep.value / totalSteps.value) * 100)
  const canContinue = computed(() => {
    switch (currentStep.value) {
      case 1: // Auth - handled by route guard
        return true
      case 2: // Connect Apps
        return connectedApps.value.length > 0
      case 3: // Integration
        return selectedIntegrations.value.length > 0
      case 4: // Configuration
        return true // Can always skip
      default:
        return false
    }
  })

  const hasConnectedApps = computed(() => connectedApps.value.length > 0)

  // Actions
  function setStep(step) {
    currentStep.value = step
  }

  function nextStep() {
    if (currentStep.value < totalSteps.value) {
      currentStep.value++
    }
  }

  function previousStep() {
    if (currentStep.value > 1) {
      currentStep.value--
    }
  }

  function connectApp(appId) {
    const app = availableApps.value.find(a => a.id === appId)
    if (app && !app.isConnected) {
      app.isConnected = true
      connectedApps.value.push(appId)
    }
  }

  function disconnectApp(appId) {
    const app = availableApps.value.find(a => a.id === appId)
    if (app) {
      app.isConnected = false
      connectedApps.value = connectedApps.value.filter(id => id !== appId)
      selectedIntegrations.value = selectedIntegrations.value.filter(
        integration => !integration.includes(appId)
      )
    }
  }

  function addIntegration(fromApp, toApp) {
    const integrationKey = `${fromApp}-${toApp}`
    if (!selectedIntegrations.value.includes(integrationKey)) {
      selectedIntegrations.value.push(integrationKey)
    }
  }

  function removeIntegration(integrationKey) {
    selectedIntegrations.value = selectedIntegrations.value.filter(
      key => key !== integrationKey
    )
  }

  function saveFieldMapping(integrationKey, mapping) {
    fieldMappings.value[integrationKey] = mapping
  }

  function completeOnboarding() {
    isCompleted.value = true
    // Reset for next time if needed
    currentStep.value = 1
  }

  function resetOnboarding() {
    currentStep.value = 1
    isCompleted.value = false
    connectedApps.value = []
    selectedIntegrations.value = []
    fieldMappings.value = {}
    availableApps.value.forEach(app => {
      app.isConnected = false
    })
  }

  return {
    // State
    currentStep,
    totalSteps,
    isCompleted,
    connectedApps,
    selectedIntegrations,
    fieldMappings,
    availableApps,

    // Computed
    progress,
    canContinue,
    hasConnectedApps,

    // Actions
    setStep,
    nextStep,
    previousStep,
    connectApp,
    disconnectApp,
    addIntegration,
    removeIntegration,
    saveFieldMapping,
    completeOnboarding,
    resetOnboarding,
  }
})
