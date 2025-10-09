<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Settings</h1>
      <p class="mt-1 text-sm text-gray-500">Manage your preferences and notification settings</p>
    </div>

    <!-- Notification Settings -->
    <AccountCard title="Notifications" description="Choose how you want to be notified">
      <div class="space-y-4">
        <div class="flex items-center justify-between py-3 border-b border-gray-200 last:border-0">
          <div class="flex-1">
            <h4 class="text-sm font-medium text-gray-900">Email Notifications</h4>
            <p class="text-sm text-gray-500">Receive email updates about your account activity</p>
          </div>
          <button
            @click="settings.emailNotifications = !settings.emailNotifications"
            :class="[
              settings.emailNotifications ? 'bg-blue-600' : 'bg-gray-200',
              'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
            ]"
          >
            <span
              :class="[
                settings.emailNotifications ? 'translate-x-6' : 'translate-x-1',
                'inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out mt-1'
              ]"
            />
          </button>
        </div>

        <div class="flex items-center justify-between py-3 border-b border-gray-200 last:border-0">
          <div class="flex-1">
            <h4 class="text-sm font-medium text-gray-900">Integration Alerts</h4>
            <p class="text-sm text-gray-500">Get notified when integrations connect or disconnect</p>
          </div>
          <button
            @click="settings.integrationAlerts = !settings.integrationAlerts"
            :class="[
              settings.integrationAlerts ? 'bg-blue-600' : 'bg-gray-200',
              'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
            ]"
          >
            <span
              :class="[
                settings.integrationAlerts ? 'translate-x-6' : 'translate-x-1',
                'inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out mt-1'
              ]"
            />
          </button>
        </div>

        <div class="flex items-center justify-between py-3 border-b border-gray-200 last:border-0">
          <div class="flex-1">
            <h4 class="text-sm font-medium text-gray-900">Workflow Notifications</h4>
            <p class="text-sm text-gray-500">Alerts when workflows complete or fail</p>
          </div>
          <button
            @click="settings.workflowNotifications = !settings.workflowNotifications"
            :class="[
              settings.workflowNotifications ? 'bg-blue-600' : 'bg-gray-200',
              'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
            ]"
          >
            <span
              :class="[
                settings.workflowNotifications ? 'translate-x-6' : 'translate-x-1',
                'inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out mt-1'
              ]"
            />
          </button>
        </div>

        <div class="flex items-center justify-between py-3">
          <div class="flex-1">
            <h4 class="text-sm font-medium text-gray-900">Marketing Emails</h4>
            <p class="text-sm text-gray-500">Receive tips, updates, and promotional content</p>
          </div>
          <button
            @click="settings.marketingEmails = !settings.marketingEmails"
            :class="[
              settings.marketingEmails ? 'bg-blue-600' : 'bg-gray-200',
              'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
            ]"
          >
            <span
              :class="[
                settings.marketingEmails ? 'translate-x-6' : 'translate-x-1',
                'inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out mt-1'
              ]"
            />
          </button>
        </div>
      </div>
    </AccountCard>

    <!-- Preferences -->
    <AccountCard title="Preferences" description="Customize your experience">
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Language</label>
          <select
            v-model="settings.language"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          >
            <option value="en">English</option>
            <option value="es">Spanish</option>
            <option value="fr">French</option>
            <option value="de">German</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Timezone</label>
          <select
            v-model="settings.timezone"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          >
            <option value="UTC">UTC</option>
            <option value="America/New_York">Eastern Time</option>
            <option value="America/Chicago">Central Time</option>
            <option value="America/Denver">Mountain Time</option>
            <option value="America/Los_Angeles">Pacific Time</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Date Format</label>
          <select
            v-model="settings.dateFormat"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          >
            <option value="MM/DD/YYYY">MM/DD/YYYY</option>
            <option value="DD/MM/YYYY">DD/MM/YYYY</option>
            <option value="YYYY-MM-DD">YYYY-MM-DD</option>
          </select>
        </div>
      </div>
    </AccountCard>

    <!-- Save Button -->
    <div class="flex justify-end">
      <button
        @click="saveSettings"
        :disabled="saving"
        class="px-6 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors disabled:opacity-50"
      >
        <span v-if="saving">Saving...</span>
        <span v-else>Save Settings</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import AccountCard from '@/components/AccountCard.vue'

const saving = ref(false)

const settings = reactive({
  emailNotifications: true,
  integrationAlerts: true,
  workflowNotifications: true,
  marketingEmails: false,
  language: 'en',
  timezone: 'America/New_York',
  dateFormat: 'MM/DD/YYYY'
})

const saveSettings = async () => {
  saving.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    alert('Settings saved successfully!')
  } catch (error) {
    console.error('Error saving settings:', error)
    alert('Failed to save settings')
  } finally {
    saving.value = false
  }
}
</script>
