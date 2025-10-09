<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Security</h1>
      <p class="mt-1 text-sm text-gray-500">Manage your password and security settings</p>
    </div>

    <!-- Change Password -->
    <AccountCard title="Change Password" description="Update your password regularly to keep your account secure">
      <form @submit.prevent="handleChangePassword" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Current Password</label>
          <input
            v-model="passwordForm.currentPassword"
            type="password"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            placeholder="Enter current password"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">New Password</label>
          <input
            v-model="passwordForm.newPassword"
            type="password"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            placeholder="Enter new password"
            minlength="8"
            required
          />
          <p class="mt-1 text-xs text-gray-500">Must be at least 8 characters long</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Confirm New Password</label>
          <input
            v-model="passwordForm.confirmPassword"
            type="password"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            placeholder="Confirm new password"
            required
          />
        </div>

        <div class="flex justify-end">
          <button
            type="submit"
            :disabled="changingPassword"
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors disabled:opacity-50"
          >
            <span v-if="changingPassword">Updating...</span>
            <span v-else>Update Password</span>
          </button>
        </div>
      </form>
    </AccountCard>

    <!-- Two-Factor Authentication -->
    <AccountCard title="Two-Factor Authentication" description="Add an extra layer of security to your account">
      <div class="flex items-center justify-between">
        <div class="flex-1">
          <h4 class="text-sm font-medium text-gray-900">2FA Status</h4>
          <p class="text-sm text-gray-500 mt-1">
            Two-factor authentication is currently <span class="font-medium">{{ twoFactorEnabled ? 'enabled' : 'disabled' }}</span>
          </p>
        </div>
        <button
          @click="toggleTwoFactor"
          :class="[
            twoFactorEnabled ? 'bg-green-600 hover:bg-green-700' : 'bg-blue-600 hover:bg-blue-700',
            'px-4 py-2 text-sm font-medium text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors'
          ]"
        >
          {{ twoFactorEnabled ? 'Disable 2FA' : 'Enable 2FA' }}
        </button>
      </div>
    </AccountCard>

    <!-- Active Sessions -->
    <AccountCard title="Active Sessions" description="Manage devices where you're currently logged in">
      <div class="space-y-3">
        <div v-for="session in activeSessions" :key="session.id" class="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
          <div class="flex items-center space-x-4">
            <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-900">{{ session.device }}</h4>
              <p class="text-xs text-gray-500">{{ session.location }} • {{ session.lastActive }}</p>
            </div>
            <span v-if="session.current" class="ml-4 px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
              Current
            </span>
          </div>
          <button
            v-if="!session.current"
            @click="revokeSession(session)"
            class="px-3 py-1.5 text-xs font-medium text-red-700 bg-red-50 border border-red-200 rounded-lg hover:bg-red-100 transition-colors"
          >
            Revoke
          </button>
        </div>
      </div>
    </AccountCard>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import AccountCard from '@/components/AccountCard.vue'

const changingPassword = ref(false)
const twoFactorEnabled = ref(false)

const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const activeSessions = ref([
  { id: 1, device: 'Chrome on Windows', location: 'New York, US', lastActive: 'Active now', current: true },
  { id: 2, device: 'Safari on MacBook Pro', location: 'San Francisco, US', lastActive: '2 hours ago', current: false },
  { id: 3, device: 'Firefox on Linux', location: 'London, UK', lastActive: '1 day ago', current: false }
])

const handleChangePassword = async () => {
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    alert('New passwords do not match!')
    return
  }

  changingPassword.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    alert('Password changed successfully!')
    passwordForm.currentPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
  } catch (error) {
    console.error('Error changing password:', error)
    alert('Failed to change password')
  } finally {
    changingPassword.value = false
  }
}

const toggleTwoFactor = () => {
  if (twoFactorEnabled.value) {
    if (confirm('Are you sure you want to disable two-factor authentication?')) {
      twoFactorEnabled.value = false
      alert('Two-factor authentication disabled')
    }
  } else {
    alert('Two-factor authentication setup coming soon!')
    // TODO: Show 2FA setup modal
  }
}

const revokeSession = (session) => {
  if (confirm(`Revoke session on ${session.device}?`)) {
    activeSessions.value = activeSessions.value.filter(s => s.id !== session.id)
    alert('Session revoked successfully')
  }
}
</script>
