<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Integrations</h1>
        <p class="mt-1 text-sm text-gray-500">Manage your connected apps and services</p>
      </div>
      <button
        @click="$router.push('/')"
        class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
      >
        Add Integration
      </button>
    </div>

    <!-- Connected Integrations -->
    <AccountCard title="Connected Apps" :description="`You have ${integrations.length} active integrations`">
      <div v-if="integrations.length === 0" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No integrations</h3>
        <p class="mt-1 text-sm text-gray-500">Get started by connecting your first app.</p>
        <div class="mt-6">
          <button
            @click="$router.push('/')"
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700"
          >
            Browse Apps
          </button>
        </div>
      </div>

      <div v-else class="space-y-3">
        <IntegrationItem
          v-for="integration in integrations"
          :key="integration.id"
          :integration="integration"
          @disconnect="handleDisconnect"
          @configure="handleConfigure"
        />
      </div>
    </AccountCard>

    <!-- Disconnect Confirmation Modal -->
    <ConfirmModal
      v-model="showDisconnectModal"
      title="Disconnect Integration"
      :description="`Are you sure you want to disconnect ${selectedIntegration?.app_name}?`"
      message="This will stop all workflows using this integration. You can reconnect at any time."
      variant="danger"
      confirmText="Disconnect"
      :loading="disconnecting"
      @confirm="confirmDisconnect"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AccountCard from '@/components/AccountCard.vue'
import IntegrationItem from '@/components/IntegrationItem.vue'
import ConfirmModal from '@/components/ConfirmModal.vue'

const router = useRouter()

const integrations = ref([
  {
    id: 1,
    app_name: 'Google Sheets',
    description: 'Spreadsheet and data management',
    status: 'active',
    connected_at: '2025-01-15'
  },
  {
    id: 2,
    app_name: 'Slack',
    description: 'Team communication platform',
    status: 'active',
    connected_at: '2025-02-01'
  },
  {
    id: 3,
    app_name: 'Xero',
    description: 'Accounting software',
    status: 'active',
    connected_at: '2025-02-20'
  }
])

const showDisconnectModal = ref(false)
const selectedIntegration = ref(null)
const disconnecting = ref(false)

const handleDisconnect = (integration) => {
  selectedIntegration.value = integration
  showDisconnectModal.value = true
}

const handleConfigure = (integration) => {
  console.log('Configure integration:', integration)
  // Navigate to the integrate page where users can manage app connections
  router.push({ name: 'Integrate' })
}

const confirmDisconnect = async () => {
  disconnecting.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    integrations.value = integrations.value.filter(i => i.id !== selectedIntegration.value.id)
    showDisconnectModal.value = false
    selectedIntegration.value = null
  } catch (error) {
    console.error('Error disconnecting:', error)
    alert('Failed to disconnect integration')
  } finally {
    disconnecting.value = false
  }
}
</script>
