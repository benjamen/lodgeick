<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Subscription</h1>
      <p class="mt-1 text-sm text-gray-500">Manage your subscription plan and billing</p>
    </div>

    <!-- Current Plan -->
    <AccountCard>
      <template #header>
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">Current Plan</h3>
            <p class="mt-1 text-sm text-gray-500">You are currently on the {{ currentPlan.name }} plan</p>
          </div>
          <span
            class="px-4 py-2 text-sm font-semibold rounded-full"
            :class="currentPlan.name === 'Free' ? 'bg-gray-100 text-gray-800' : 'bg-blue-100 text-blue-800'"
          >
            {{ currentPlan.name }}
          </span>
        </div>
      </template>

      <div class="space-y-4">
        <div class="flex items-baseline">
          <span class="text-4xl font-bold text-gray-900">${{ currentPlan.price }}</span>
          <span class="ml-2 text-gray-500">/month</span>
        </div>

        <ul class="space-y-3">
          <li v-for="feature in currentPlan.features" :key="feature" class="flex items-start">
            <svg class="w-5 h-5 text-green-500 mr-3 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            <span class="text-sm text-gray-700">{{ feature }}</span>
          </li>
        </ul>

        <div class="pt-4 border-t border-gray-200">
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-500">Next billing date</span>
            <span class="font-medium text-gray-900">{{ nextBillingDate }}</span>
          </div>
        </div>
      </div>
    </AccountCard>

    <!-- Available Plans -->
    <div>
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Available Plans</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div
          v-for="plan in availablePlans"
          :key="plan.id"
          class="bg-white border-2 rounded-xl p-6 transition-all hover:shadow-lg"
          :class="plan.name === currentPlan.name ? 'border-blue-500' : 'border-gray-200'"
        >
          <h4 class="text-lg font-semibold text-gray-900">{{ plan.name }}</h4>
          <div class="mt-4 flex items-baseline">
            <span class="text-3xl font-bold">${{ plan.price }}</span>
            <span class="ml-1 text-gray-500">/month</span>
          </div>
          <ul class="mt-6 space-y-3">
            <li v-for="feature in plan.features" :key="feature" class="flex items-start text-sm">
              <svg class="w-4 h-4 text-green-500 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              <span class="text-gray-600">{{ feature }}</span>
            </li>
          </ul>
          <button
            v-if="plan.name !== currentPlan.name"
            @click="changePlan(plan)"
            class="mt-6 w-full px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
          >
            {{ plan.price > currentPlan.price ? 'Upgrade' : 'Downgrade' }}
          </button>
          <button
            v-else
            disabled
            class="mt-6 w-full px-4 py-2 text-sm font-medium text-gray-400 bg-gray-100 rounded-lg cursor-not-allowed"
          >
            Current Plan
          </button>
        </div>
      </div>
    </div>

    <!-- Payment History -->
    <AccountCard title="Payment History" description="View your recent transactions">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="payment in paymentHistory" :key="payment.id">
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{{ payment.date }}</td>
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-600">{{ payment.description }}</td>
              <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">${{ payment.amount }}</td>
              <td class="px-4 py-3 whitespace-nowrap">
                <span
                  class="px-2 py-1 text-xs font-medium rounded-full"
                  :class="payment.status === 'paid' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                >
                  {{ payment.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </AccountCard>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AccountCard from '@/components/AccountCard.vue'

const currentPlan = ref({
  name: 'Pro',
  price: 29,
  features: [
    '50 integrations',
    'Unlimited workflows',
    'Advanced analytics',
    'Priority support',
    'Custom branding'
  ]
})

const nextBillingDate = ref('April 1, 2025')

const availablePlans = ref([
  {
    id: 1,
    name: 'Free',
    price: 0,
    features: ['5 integrations', '10 workflows', 'Basic analytics', 'Email support']
  },
  {
    id: 2,
    name: 'Pro',
    price: 29,
    features: ['50 integrations', 'Unlimited workflows', 'Advanced analytics', 'Priority support', 'Custom branding']
  },
  {
    id: 3,
    name: 'Enterprise',
    price: 99,
    features: ['Unlimited integrations', 'Unlimited workflows', 'Advanced analytics', '24/7 support', 'Custom branding', 'Dedicated account manager', 'SLA guarantee']
  }
])

const paymentHistory = ref([
  { id: 1, date: 'Mar 1, 2025', description: 'Pro Plan - Monthly', amount: 29, status: 'paid' },
  { id: 2, date: 'Feb 1, 2025', description: 'Pro Plan - Monthly', amount: 29, status: 'paid' },
  { id: 3, date: 'Jan 1, 2025', description: 'Pro Plan - Monthly', amount: 29, status: 'paid' }
])

const changePlan = (plan) => {
  if (confirm(`Are you sure you want to change to the ${plan.name} plan?`)) {
    console.log('Changing plan to:', plan.name)
    // TODO: Implement plan change
  }
}
</script>
