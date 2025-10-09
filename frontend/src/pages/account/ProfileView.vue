<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Profile Settings</h1>
      <p class="mt-1 text-sm text-gray-500">Manage your personal information and avatar</p>
    </div>

    <!-- Avatar Section -->
    <AccountCard title="Profile Picture" description="Upload a new avatar or update your existing one">
      <div class="flex items-center space-x-6">
        <div class="flex-shrink-0">
          <div class="w-24 h-24 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center text-white font-bold text-3xl shadow-lg">
            {{ userInitials }}
          </div>
        </div>
        <div class="flex-1">
          <h4 class="text-sm font-medium text-gray-900">Change Avatar</h4>
          <p class="text-sm text-gray-500 mt-1">JPG, GIF or PNG. Max size of 2MB.</p>
          <div class="mt-3 flex space-x-3">
            <button
              @click="triggerFileUpload"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
            >
              Upload New
            </button>
            <button
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors"
            >
              Remove
            </button>
          </div>
          <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="handleFileChange" />
        </div>
      </div>
    </AccountCard>

    <!-- Personal Information -->
    <AccountCard title="Personal Information" description="Update your personal details">
      <form @submit.prevent="handleSaveProfile" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">First Name</label>
            <input
              v-model="profileForm.first_name"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              placeholder="John"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Last Name</label>
            <input
              v-model="profileForm.last_name"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              placeholder="Doe"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
          <input
            v-model="profileForm.email"
            type="email"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            placeholder="john@example.com"
          />
          <p class="mt-1 text-xs text-gray-500">Your email is used for login and notifications</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Phone Number</label>
          <input
            v-model="profileForm.phone"
            type="tel"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            placeholder="+1 (555) 123-4567"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Bio</label>
          <textarea
            v-model="profileForm.bio"
            rows="4"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors resize-none"
            placeholder="Tell us about yourself..."
          ></textarea>
        </div>

        <div class="flex justify-end space-x-3 pt-4">
          <button
            type="button"
            @click="resetForm"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="saving"
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="saving" class="inline-flex items-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Saving...
            </span>
            <span v-else>Save Changes</span>
          </button>
        </div>
      </form>
    </AccountCard>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { session } from '@/data/session'
import AccountCard from '@/components/AccountCard.vue'

const fileInput = ref(null)
const saving = ref(false)

const profileForm = reactive({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  bio: ''
})

const userInitials = computed(() => {
  const fullName = `${profileForm.first_name} ${profileForm.last_name}`.trim()
  if (!fullName) return session.user?.[0]?.toUpperCase() || 'U'

  return fullName
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Handle file upload
    console.log('File selected:', file.name)
    // TODO: Implement file upload to server
  }
}

const handleSaveProfile = async () => {
  saving.value = true
  try {
    // TODO: Implement API call to save profile
    await new Promise(resolve => setTimeout(resolve, 1000))
    console.log('Profile saved:', profileForm)
    alert('Profile updated successfully!')
  } catch (error) {
    console.error('Error saving profile:', error)
    alert('Failed to save profile. Please try again.')
  } finally {
    saving.value = false
  }
}

const resetForm = () => {
  // Reset to original values
  loadProfile()
}

const loadProfile = () => {
  // TODO: Load from API
  profileForm.first_name = session.user_fullname?.split(' ')[0] || ''
  profileForm.last_name = session.user_fullname?.split(' ').slice(1).join(' ') || ''
  profileForm.email = session.user || ''
  profileForm.phone = ''
  profileForm.bio = ''
}

onMounted(() => {
  loadProfile()
})
</script>
