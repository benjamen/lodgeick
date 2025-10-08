<template>
  <div class="landing-page">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark position-absolute w-100 z-index-3">
      <div class="container">
        <a class="navbar-brand" href="#">
          <span class="text-white font-weight-bold">Lodgeick</span>
        </a>
        <button
          class="navbar-toggler shadow-none ms-2"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navigation">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a class="nav-link text-white">{{ session.user }}</a>
            </li>
            <li class="nav-item">
              <button @click="session.logout.submit()" class="btn btn-sm btn-white mb-0">
                Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <header class="hero-section">
      <div
        class="page-header min-vh-75"
        style="background-image: url('https://images.unsplash.com/photo-1557804506-669a67965ba0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1974&q=80')"
      >
        <span class="mask bg-gradient-dark opacity-6"></span>
        <div class="container">
          <div class="row justify-content-center">
            <div class="col-lg-8 text-center mx-auto my-auto">
              <h1 class="text-white mb-4 display-3 font-weight-bold">
                Connect Your Apps in
                <span class="text-gradient-primary">One Click</span>
              </h1>
              <p class="lead text-white mb-5 opacity-8">
                Automate workflows between your favorite business apps without writing a single line of code.
                50+ integrations ready to deploy instantly.
              </p>
              <div class="search-wrapper">
                <div class="input-group input-group-lg input-group-outline bg-white rounded-pill shadow-lg p-2">
                  <span class="input-group-text border-0 bg-transparent">
                    <i class="fas fa-search text-muted"></i>
                  </span>
                  <input
                    type="text"
                    class="form-control border-0"
                    placeholder="Search for apps like Xero, Slack, Gmail..."
                    v-model="searchQuery"
                  />
                </div>
              </div>
              <div class="mt-4">
                <a href="#catalog" class="btn btn-white btn-lg shadow-lg mb-2">
                  Browse Catalog
                  <i class="fas fa-arrow-down ms-2"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Stats Section -->
    <section class="py-5 bg-gradient-dark position-relative">
      <div class="container">
        <div class="row text-center">
          <div class="col-lg-3 col-md-6">
            <div class="info">
              <div class="icon icon-shape bg-gradient-primary shadow-primary text-center rounded-circle mx-auto mb-3">
                <i class="fas fa-plug text-lg opacity-10"></i>
              </div>
              <h3 class="text-white font-weight-bold">50+</h3>
              <p class="text-white opacity-8">Integrations</p>
            </div>
          </div>
          <div class="col-lg-3 col-md-6">
            <div class="info">
              <div class="icon icon-shape bg-gradient-info shadow-info text-center rounded-circle mx-auto mb-3">
                <i class="fas fa-bolt text-lg opacity-10"></i>
              </div>
              <h3 class="text-white font-weight-bold">1-Click</h3>
              <p class="text-white opacity-8">Setup Time</p>
            </div>
          </div>
          <div class="col-lg-3 col-md-6">
            <div class="info">
              <div class="icon icon-shape bg-gradient-success shadow-success text-center rounded-circle mx-auto mb-3">
                <i class="fas fa-shield-alt text-lg opacity-10"></i>
              </div>
              <h3 class="text-white font-weight-bold">100%</h3>
              <p class="text-white opacity-8">Secure OAuth</p>
            </div>
          </div>
          <div class="col-lg-3 col-md-6">
            <div class="info">
              <div class="icon icon-shape bg-gradient-warning shadow-warning text-center rounded-circle mx-auto mb-3">
                <i class="fas fa-chart-line text-lg opacity-10"></i>
              </div>
              <h3 class="text-white font-weight-bold">Real-time</h3>
              <p class="text-white opacity-8">Monitoring</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- App Catalog Section -->
    <section id="catalog" class="py-7 bg-gray-100">
      <div class="container">
        <div class="row mb-5">
          <div class="col-lg-8 mx-auto text-center">
            <h2 class="display-4 font-weight-bold mb-3">Popular Integrations</h2>
            <p class="lead text-muted">
              Connect your business apps and automate workflows in seconds
            </p>
          </div>
        </div>

        <!-- Category Pills -->
        <div class="row mb-4">
          <div class="col-12">
            <div class="d-flex justify-content-center flex-wrap gap-2">
              <button
                v-for="cat in categories"
                :key="cat"
                @click="selectedCategory = cat"
                :class="[
                  'btn btn-outline-dark btn-sm rounded-pill',
                  selectedCategory === cat ? 'active' : ''
                ]"
              >
                {{ cat || 'All' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="catalog.loading" class="text-center py-7">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="text-muted mt-3">Loading integrations...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="catalog.error" class="text-center py-7">
          <div class="alert alert-danger d-inline-block">
            <i class="fas fa-exclamation-triangle me-2"></i>
            Error loading catalog: {{ catalog.error }}
          </div>
          <br />
          <button @click="catalog.fetch()" class="btn btn-primary mt-3">
            <i class="fas fa-redo me-2"></i>Retry
          </button>
        </div>

        <!-- App Cards Grid -->
        <div v-else class="row g-4">
          <div
            v-for="app in filteredApps"
            :key="app.name"
            class="col-lg-4 col-md-6"
          >
            <div
              class="card card-app h-100 shadow-sm hover-lift"
              @click="selectApp(app)"
              role="button"
            >
              <div class="card-body p-4">
                <div class="d-flex align-items-start mb-3">
                  <div class="app-icon me-3">
                    <div class="avatar avatar-xl bg-gradient-primary shadow-primary">
                      <span class="text-white font-weight-bold text-lg">
                        {{ app.display_name.charAt(0) }}
                      </span>
                    </div>
                  </div>
                  <div class="flex-fill">
                    <h5 class="card-title font-weight-bold mb-1">
                      {{ app.display_name }}
                    </h5>
                    <span class="badge bg-gradient-info text-xs">
                      {{ app.category }}
                    </span>
                  </div>
                </div>
                <p class="card-text text-muted text-sm mb-3">
                  {{ app.description || 'Connect and automate your workflows' }}
                </p>
                <div class="d-flex align-items-center justify-content-between">
                  <small class="text-muted">
                    <i class="fas fa-puzzle-piece me-1"></i>
                    {{ app.use_cases?.length || 0 }} use cases
                  </small>
                  <div>
                    <span v-if="app.isConnected" class="badge bg-gradient-success me-2">
                      <i class="fas fa-check me-1"></i>Connected
                    </span>
                    <i class="fas fa-arrow-right text-primary"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div
          v-if="!catalog.loading && !catalog.error && filteredApps.length === 0"
          class="text-center py-7"
        >
          <div class="icon icon-shape bg-gradient-primary shadow-primary mx-auto mb-4">
            <i class="fas fa-search text-2xl opacity-10"></i>
          </div>
          <h4 class="font-weight-bold mb-2">No apps found</h4>
          <p class="text-muted">
            Try adjusting your search or category filter
          </p>
        </div>
      </div>
    </section>

    <!-- App Details Modal -->
    <div
      class="modal fade"
      :class="{ show: showAppDialog, 'd-block': showAppDialog }"
      tabindex="-1"
      :style="{ backgroundColor: showAppDialog ? 'rgba(0,0,0,0.5)' : '' }"
      @click.self="showAppDialog = false"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content" v-if="selectedApp">
          <div class="modal-header bg-gradient-primary">
            <h5 class="modal-title text-white font-weight-bold">
              <div class="avatar avatar-sm bg-white shadow me-2 d-inline-flex align-items-center justify-content-center">
                <span class="text-primary font-weight-bold">
                  {{ selectedApp.display_name.charAt(0) }}
                </span>
              </div>
              {{ selectedApp.display_name }}
            </h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              @click="showAppDialog = false"
            ></button>
          </div>
          <div class="modal-body p-4">
            <p class="text-muted mb-4">{{ selectedApp.description }}</p>

            <div class="mb-4">
              <span class="badge bg-gradient-info me-2">{{ selectedApp.category }}</span>
              <span class="badge bg-gradient-success">OAuth Enabled</span>
            </div>

            <h6 class="font-weight-bold mb-3">
              <i class="fas fa-puzzle-piece me-2 text-primary"></i>
              Available Use Cases
            </h6>
            <div class="list-group list-group-flush">
              <div
                v-for="useCase in selectedApp.use_cases"
                :key="useCase.use_case_name"
                class="list-group-item list-group-item-action hover-bg-light rounded mb-2"
                @click="activateUseCase(useCase)"
                role="button"
              >
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <h6 class="mb-1 font-weight-bold">{{ useCase.use_case_name }}</h6>
                    <p class="mb-0 text-sm text-muted">
                      {{ useCase.description || 'Automate your workflow with this integration' }}
                    </p>
                  </div>
                  <i class="fas fa-chevron-right text-muted"></i>
                </div>
              </div>
              <div v-if="!selectedApp.use_cases || selectedApp.use_cases.length === 0" class="text-center py-4">
                <p class="text-muted mb-0">No use cases configured yet</p>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="showAppDialog = false"
            >
              Close
            </button>
            <button
              v-if="!selectedApp?.isConnected"
              type="button"
              class="btn btn-primary"
              @click="connectApp"
            >
              <i class="fas fa-plug me-2"></i>
              Connect App
            </button>
            <button
              v-else
              type="button"
              class="btn btn-success"
              disabled
            >
              <i class="fas fa-check me-2"></i>
              Connected
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- OAuth Setup Wizard -->
    <OAuthSetupWizard
      :show="showSetupWizard"
      :provider="selectedApp?.oauth_provider || 'google'"
      @close="closeSetupWizard"
      @success="handleSetupSuccess"
    />

    <!-- Authentication Required Modal -->
    <div
      class="modal fade"
      :class="{ show: showAuthModal, 'd-block': showAuthModal }"
      tabindex="-1"
      :style="{ backgroundColor: showAuthModal ? 'rgba(0,0,0,0.5)' : '' }"
      @click.self="showAuthModal = false"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-gradient-primary">
            <h5 class="modal-title text-white font-weight-bold">
              <i class="fas fa-lock me-2"></i>
              Authentication Required
            </h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              @click="showAuthModal = false"
            ></button>
          </div>
          <div class="modal-body p-4 text-center">
            <div class="icon icon-shape bg-gradient-primary shadow-primary rounded-circle mx-auto mb-4">
              <i class="fas fa-user-plus text-2xl opacity-10 text-white"></i>
            </div>
            <h4 class="font-weight-bold mb-3">Sign in to Connect Apps</h4>
            <p class="text-muted mb-4">
              Create a free account or sign in to save your app connections and start automating your workflows.
            </p>
            <div class="d-grid gap-2">
              <router-link to="/account/signup" class="btn btn-primary btn-lg">
                <i class="fas fa-user-plus me-2"></i>
                Create Free Account
              </router-link>
              <router-link to="/account/login" class="btn btn-outline-secondary">
                <i class="fas fa-sign-in-alt me-2"></i>
                Sign In
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { createResource } from "frappe-ui"
import { session } from "../data/session"
import OAuthSetupWizard from "../components/OAuthSetupWizard.vue"

const searchQuery = ref("")
const showAppDialog = ref(false)
const selectedApp = ref(null)
const selectedCategory = ref(null)
const showSetupWizard = ref(false)
const showAuthModal = ref(false)

// Fetch app catalog
const catalog = createResource({
  url: "lodgeick.api.catalog.get_app_catalog",
  auto: true,
})

// Fetch user's connected integrations
const userIntegrations = createResource({
  url: "lodgeick.lodgeick.doctype.user_integration_settings.user_integration_settings.get_user_integrations",
  auto: session.isLoggedIn,
})

// Get unique categories
const categories = computed(() => {
  if (!catalog.data?.apps) return [null]
  const cats = [null, ...new Set(catalog.data.apps.map(app => app.category).filter(Boolean))]
  return cats
})

// Check if app is connected
function isAppConnected(appName) {
  if (!userIntegrations.data) return false
  return userIntegrations.data.some(integration => integration.app_name === appName)
}

// Filter apps based on search and category
const filteredApps = computed(() => {
  if (!catalog.data?.apps) return []

  let apps = catalog.data.apps.map(app => ({
    ...app,
    isConnected: isAppConnected(app.name)
  }))

  // Filter by category
  if (selectedCategory.value) {
    apps = apps.filter(app => app.category === selectedCategory.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    apps = apps.filter(
      app =>
        app.display_name.toLowerCase().includes(query) ||
        app.description?.toLowerCase().includes(query) ||
        app.category?.toLowerCase().includes(query)
    )
  }

  return apps
})

function selectApp(app) {
  selectedApp.value = app
  showAppDialog.value = true
}

// OAuth connection resource
const initiateOAuth = createResource({
  url: "lodgeick.api.oauth.initiate_oauth",
  makeParams(values) {
    return {
      provider: values.provider
      // Let backend determine redirect_uri automatically
    }
  },
  onSuccess(data) {
    if (data.authorization_url) {
      // Open OAuth popup
      const width = 600
      const height = 700
      const left = window.screen.width / 2 - width / 2
      const top = window.screen.height / 2 - height / 2

      const popup = window.open(
        data.authorization_url,
        "OAuth",
        `width=${width},height=${height},left=${left},top=${top}`
      )

      // Poll for popup closure
      const pollTimer = setInterval(() => {
        if (popup && popup.closed) {
          clearInterval(pollTimer)
          // Refresh the page to show connected state
          catalog.fetch()
          showAppDialog.value = false
        }
      }, 500)
    }
  },
  onError(error) {
    // Extract error message from frappe error object
    let errorMsg = ''
    if (error.messages && error.messages.length > 0) {
      errorMsg = error.messages[0]
    } else if (error.message) {
      errorMsg = error.message
    } else {
      errorMsg = error.toString()
    }

    // Check if error is due to missing credentials
    if (errorMsg.includes('not configured') || errorMsg.includes('credentials') || errorMsg.includes('None')) {
      // Show setup wizard instead of alert (this is expected behavior)
      console.log('OAuth credentials not configured, opening setup wizard...')
      showAppDialog.value = false
      showSetupWizard.value = true
    } else {
      alert(`Failed to connect: ${errorMsg}`)
    }
  }
})

function connectApp() {
  // Check if user is logged in
  if (!session.isLoggedIn) {
    // Close the app dialog and show auth modal
    showAppDialog.value = false
    showAuthModal.value = true
    return
  }

  if (!selectedApp.value?.oauth_provider) {
    alert("OAuth provider not configured for this app")
    return
  }

  // Try to initiate OAuth
  initiateOAuth.submit({
    provider: selectedApp.value.oauth_provider
  })
}

function handleOAuthError(error) {
  // Check if error is due to missing credentials
  if (error.includes('not configured') || error.includes('client_id') || error.includes('None')) {
    // Show setup wizard
    showAppDialog.value = false
    showSetupWizard.value = true
  } else {
    alert(`Failed to connect: ${error}`)
  }
}

function closeSetupWizard() {
  showSetupWizard.value = false
}

function handleSetupSuccess(credentials) {
  // Credentials saved, now we can try OAuth again
  alert(`Credentials saved! You can now click "Connect App" to authenticate.`)
}

function activateUseCase(useCase) {
  // TODO: Implement integration activation
  alert(`Activating: ${useCase.use_case_name}`)
  showAppDialog.value = false
}
</script>

<style scoped>
.landing-page {
  background: #f8f9fa;
}

.hero-section {
  position: relative;
}

.page-header {
  min-height: 75vh;
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: center;
}

.mask {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.page-header .container {
  position: relative;
  z-index: 2;
}

.bg-gradient-dark {
  background: linear-gradient(310deg, #141727 0%, #3A416F 100%);
}

.bg-gradient-primary {
  background: linear-gradient(310deg, #7928CA 0%, #FF0080 100%);
}

.bg-gradient-info {
  background: linear-gradient(310deg, #2152FF 0%, #21D4FD 100%);
}

.bg-gradient-success {
  background: linear-gradient(310deg, #17AD37 0%, #98EC2D 100%);
}

.bg-gradient-warning {
  background: linear-gradient(310deg, #F53939 0%, #FBCF33 100%);
}

.text-gradient-primary {
  background: linear-gradient(310deg, #7928CA 0%, #FF0080 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.rounded-pill {
  border-radius: 50rem !important;
}

.shadow-lg {
  box-shadow: 0 8px 26px -4px rgba(20, 20, 20, 0.15), 0 8px 9px -5px rgba(20, 20, 20, 0.06) !important;
}

.search-wrapper {
  max-width: 600px;
  margin: 0 auto;
}

.icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-shape {
  width: 64px;
  height: 64px;
  border-radius: 0.75rem;
}

.shadow-primary {
  box-shadow: 0 4px 20px 0 rgba(121, 40, 202, 0.4) !important;
}

.shadow-info {
  box-shadow: 0 4px 20px 0 rgba(33, 82, 255, 0.4) !important;
}

.shadow-success {
  box-shadow: 0 4px 20px 0 rgba(23, 173, 55, 0.4) !important;
}

.shadow-warning {
  box-shadow: 0 4px 20px 0 rgba(245, 57, 57, 0.4) !important;
}

.card-app {
  border: none;
  transition: all 0.3s ease;
  cursor: pointer;
}

.card-app:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
}

.hover-lift {
  transition: all 0.3s ease;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 0.75rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.avatar-xl {
  width: 64px;
  height: 64px;
}

.avatar-sm {
  width: 32px;
  height: 32px;
}

.btn-outline-dark.active {
  background-color: #344767;
  color: white;
}

.list-group-item-action:hover {
  background-color: #f8f9fa;
}

.hover-bg-light:hover {
  background-color: #f8f9fa;
}

.z-index-3 {
  z-index: 3;
}

.font-weight-bold {
  font-weight: 700;
}

.navbar-dark .navbar-brand {
  color: #fff;
  font-size: 1.25rem;
  font-weight: 700;
}

.btn-white {
  background-color: white;
  color: #344767;
}

.btn-white:hover {
  background-color: #f8f9fa;
}

@media (max-width: 768px) {
  .display-3 {
    font-size: 2.5rem;
  }
}
</style>
