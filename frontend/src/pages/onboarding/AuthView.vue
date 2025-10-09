<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex flex-col">
    <!-- Header with Logo -->
    <div class="p-6">
      <router-link to="/" class="inline-flex items-center gap-3 group no-underline">
        <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
          <span class="text-white font-bold text-xl">L</span>
        </div>
        <span class="text-2xl font-bold text-gray-900">Lodgeick</span>
      </router-link>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8">
      <div class="w-full max-w-md">
        <!-- Progress Bar (hidden on auth step) -->
        <!-- <StepProgressBar :current-step="1" :total-steps="4" /> -->

        <!-- Auth Card -->
        <div class="bg-white rounded-2xl shadow-xl p-8">
          <!-- Header -->
          <div class="text-center mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">
              {{ isLogin ? 'Welcome back' : 'Get started' }}
            </h1>
            <p class="text-gray-600">
              {{ isLogin ? 'Sign in to your account' : 'Create your account to continue' }}
            </p>
          </div>

          <!-- Tab Switcher -->
          <div class="flex gap-2 mb-6 p-1 bg-gray-100 rounded-lg">
            <button
              class="flex-1 py-2 text-sm font-medium rounded-md transition-all"
              :class="isLogin ? 'bg-white shadow-sm text-gray-900' : 'text-gray-600 hover:text-gray-900'"
              @click="isLogin = true"
            >
              Log In
            </button>
            <button
              class="flex-1 py-2 text-sm font-medium rounded-md transition-all"
              :class="!isLogin ? 'bg-white shadow-sm text-gray-900' : 'text-gray-600 hover:text-gray-900'"
              @click="isLogin = false"
            >
              Sign Up
            </button>
          </div>

          <!-- Login Form -->
          <form v-if="isLogin" @submit.prevent="handleLogin" class="space-y-4">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                id="email"
                v-model="loginForm.email"
                type="email"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="you@example.com"
              />
            </div>

            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                id="password"
                v-model="loginForm.password"
                type="password"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="••••••••"
              />
            </div>

            <div class="flex items-center justify-between text-sm">
              <label class="flex items-center">
                <input
                  v-model="loginForm.remember"
                  type="checkbox"
                  class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span class="ml-2 text-gray-600">Remember me</span>
              </label>
              <a href="#" class="text-blue-600 hover:text-blue-700 font-medium">
                Forgot password?
              </a>
            </div>

            <PrimaryButton
              type="submit"
              full-width
              :loading="isLoading"
              label="Sign In"
            />
          </form>

          <!-- Signup Form -->
          <form v-else @submit.prevent="handleSignup" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="firstName" class="block text-sm font-medium text-gray-700 mb-1">
                  First Name
                </label>
                <input
                  id="firstName"
                  v-model="signupForm.firstName"
                  type="text"
                  required
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="John"
                />
              </div>
              <div>
                <label for="lastName" class="block text-sm font-medium text-gray-700 mb-1">
                  Last Name
                </label>
                <input
                  id="lastName"
                  v-model="signupForm.lastName"
                  type="text"
                  required
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Doe"
                />
              </div>
            </div>

            <div>
              <label for="signup-email" class="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                id="signup-email"
                v-model="signupForm.email"
                type="email"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="you@example.com"
              />
            </div>

            <div>
              <label for="signup-password" class="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                id="signup-password"
                v-model="signupForm.password"
                type="password"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="••••••••"
              />
            </div>

            <div class="text-sm">
              <label class="flex items-start">
                <input
                  v-model="signupForm.terms"
                  type="checkbox"
                  required
                  class="mt-0.5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span class="ml-2 text-gray-600">
                  I agree to the
                  <a href="#" class="text-blue-600 hover:text-blue-700 font-medium">Terms of Service</a>
                  and
                  <a href="#" class="text-blue-600 hover:text-blue-700 font-medium">Privacy Policy</a>
                </span>
              </label>
            </div>

            <PrimaryButton
              type="submit"
              full-width
              :loading="isLoading"
              label="Create Account"
            />
          </form>

          <!-- Divider -->
          <div class="relative my-6">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300" />
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white text-gray-500">Or continue with</span>
            </div>
          </div>

          <!-- OAuth Buttons -->
          <div class="space-y-3">
            <button
              type="button"
              class="w-full flex items-center justify-center gap-3 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="#34A853"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="#EA4335"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
              <span class="text-sm font-medium text-gray-700">Google</span>
            </button>
          </div>
        </div>

        <!-- Footer -->
        <p class="mt-8 text-center text-sm text-gray-600">
          By signing in, you'll start your journey to seamless integrations
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { session } from '@/data/session'
import PrimaryButton from '@/components/onboarding/PrimaryButton.vue'
import { useOnboardingStore } from '@/stores/onboarding'

const router = useRouter()
const onboardingStore = useOnboardingStore()

const isLogin = ref(true)
const isLoading = ref(false)

const loginForm = ref({
  email: '',
  password: '',
  remember: false,
})

const signupForm = ref({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  terms: false,
})

const handleLogin = async () => {
  isLoading.value = true
  try {
    await session.login.submit({
      email: loginForm.value.email,
      password: loginForm.value.password,
    })

    // Set onboarding step and redirect
    onboardingStore.setStep(2)
    router.push({ name: 'ConnectApps' })
  } catch (error) {
    console.error('Login failed:', error)
    alert('Login failed. Please check your credentials.')
  } finally {
    isLoading.value = false
  }
}

const handleSignup = async () => {
  isLoading.value = true
  try {
    await session.signup.submit({
      email: signupForm.value.email,
      first_name: signupForm.value.firstName,
      last_name: signupForm.value.lastName,
      password: signupForm.value.password,
    })

    // Set onboarding step and redirect
    onboardingStore.setStep(2)
    router.push({ name: 'ConnectApps' })
  } catch (error) {
    console.error('Signup failed:', error)
    alert('Signup failed. Please try again.')
  } finally {
    isLoading.value = false
  }
}
</script>
