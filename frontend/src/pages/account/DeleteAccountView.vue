<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Delete Account</h1>
      <p class="mt-1 text-sm text-gray-500">Permanently delete your account and all associated data</p>
    </div>

    <!-- Danger Zone -->
    <AccountCard>
      <div class="space-y-6">
        <!-- Warning Banner -->
        <div class="bg-red-50 border-l-4 border-red-600 p-4 rounded-lg">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Warning</h3>
              <p class="mt-2 text-sm text-red-700">
                This action cannot be undone. This will permanently delete your account and remove all your data from our servers.
              </p>
            </div>
          </div>
        </div>

        <!-- What will be deleted -->
        <div>
          <h3 class="text-sm font-semibold text-gray-900 mb-3">What will be deleted:</h3>
          <ul class="space-y-2">
            <li class="flex items-start text-sm text-gray-700">
              <svg class="w-5 h-5 text-red-500 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
              <span>Your profile and personal information</span>
            </li>
            <li class="flex items-start text-sm text-gray-700">
              <svg class="w-5 h-5 text-red-500 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
              <span>All connected integrations and their data</span>
            </li>
            <li class="flex items-start text-sm text-gray-700">
              <svg class="w-5 h-5 text-red-500 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
              <span>All workflows and automation rules</span>
            </li>
            <li class="flex items-start text-sm text-gray-700">
              <svg class="w-5 h-5 text-red-500 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
              <span>Subscription and billing history</span>
            </li>
            <li class="flex items-start text-sm text-gray-700">
              <svg class="w-5 h-5 text-red-500 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
              <span>All saved preferences and settings</span>
            </li>
          </ul>
        </div>

        <!-- Confirmation Input -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            To confirm deletion, please type <span class="font-semibold text-red-600">DELETE</span> in the box below:
          </label>
          <input
            v-model="confirmText"
            type="text"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors"
            placeholder="Type DELETE to confirm"
          />
        </div>

        <!-- Delete Button -->
        <div class="flex justify-between items-center pt-4 border-t border-gray-200">
          <p class="text-sm text-gray-500">This action is irreversible. Please be certain.</p>
          <button
            @click="showDeleteModal = true"
            :disabled="confirmText !== 'DELETE'"
            class="px-6 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Delete Account
          </button>
        </div>
      </div>
    </AccountCard>

    <!-- Delete Confirmation Modal -->
    <ConfirmModal
      v-model="showDeleteModal"
      title="Delete Account"
      description="Are you absolutely sure?"
      variant="danger"
      confirmText="Yes, delete my account"
      :loading="deleting"
      @confirm="confirmDelete"
    >
      <div class="space-y-4">
        <p class="text-sm text-gray-600">
          This is your last chance. Once you delete your account:
        </p>
        <ul class="space-y-2 text-sm text-gray-600">
          <li class="flex items-start">
            <span class="font-semibold mr-2">•</span>
            <span>All your data will be permanently erased</span>
          </li>
          <li class="flex items-start">
            <span class="font-semibold mr-2">•</span>
            <span>Active integrations will be disconnected</span>
          </li>
          <li class="flex items-start">
            <span class="font-semibold mr-2">•</span>
            <span>Your subscription will be cancelled</span>
          </li>
          <li class="flex items-start">
            <span class="font-semibold mr-2">•</span>
            <span>You will not be able to recover this account</span>
          </li>
        </ul>
      </div>
    </ConfirmModal>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { session } from '@/data/session'
import AccountCard from '@/components/AccountCard.vue'
import ConfirmModal from '@/components/ConfirmModal.vue'

const router = useRouter()
const confirmText = ref('')
const showDeleteModal = ref(false)
const deleting = ref(false)

const confirmDelete = async () => {
  deleting.value = true
  try {
    // TODO: Implement actual account deletion API call
    await new Promise(resolve => setTimeout(resolve, 2000))

    // Log out and redirect
    session.logout.submit()
    router.push('/')
  } catch (error) {
    console.error('Error deleting account:', error)
    alert('Failed to delete account. Please try again or contact support.')
  } finally {
    deleting.value = false
  }
}
</script>
