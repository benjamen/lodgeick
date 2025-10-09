<template>
  <div
    class="modal fade"
    :class="{ show: show, 'd-block': show }"
    tabindex="-1"
    :style="{ backgroundColor: show ? 'rgba(0,0,0,0.5)' : '' }"
    @click.self="closeWizard"
  >
    <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <!-- Header -->
        <div class="modal-header bg-gradient-primary">
          <h5 class="modal-title text-white font-weight-bold">
            <i class="fas fa-magic me-2"></i>
            OAuth Setup Wizard - {{ providerName }}
          </h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            @click="closeWizard"
          ></button>
        </div>

        <!-- Body -->
        <div class="modal-body p-4">
          <!-- Progress Steps -->
          <div class="row mb-4">
            <div class="col-12">
              <div class="d-flex justify-content-between align-items-center">
                <div
                  v-for="(step, index) in steps"
                  :key="index"
                  class="flex-fill text-center position-relative"
                >
                  <div
                    class="step-circle mx-auto mb-2"
                    :class="{
                      'active': currentStep === index,
                      'completed': currentStep > index
                    }"
                  >
                    <i v-if="currentStep > index" class="fas fa-check"></i>
                    <span v-else>{{ index + 1 }}</span>
                  </div>
                  <small class="d-block text-muted">{{ step.title }}</small>
                  <div
                    v-if="index < steps.length - 1"
                    class="step-line"
                    :class="{ 'completed': currentStep > index }"
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Step Content -->
          <div class="step-content">
            <!-- Step 0: Create Google Cloud Project -->
            <div v-if="currentStep === 0" class="step">
              <h5 class="font-weight-bold mb-3">
                <i class="fab fa-google text-primary me-2"></i>
                Create Google Cloud Project
              </h5>
              <div class="alert alert-info">
                <i class="fas fa-info-circle me-2"></i>
                You'll need a Google account to create a Cloud project.
              </div>
              <ol class="setup-steps">
                <li class="mb-3">
                  Go to <a href="https://console.cloud.google.com" target="_blank" class="text-primary">
                    <strong>Google Cloud Console</strong>
                    <i class="fas fa-external-link-alt ms-1 small"></i>
                  </a>
                </li>
                <li class="mb-3">
                  Click the project dropdown at the top
                  <br><small class="text-muted">It usually says "Select a project" or shows your current project</small>
                </li>
                <li class="mb-3">
                  Click <strong>"New Project"</strong> in the top right
                </li>
                <li class="mb-3">
                  Name your project (e.g., "Lodgeick Integration")
                </li>
                <li class="mb-3">
                  Click <strong>"Create"</strong> and wait for the project to be created
                </li>
              </ol>
              <div class="text-center mt-4">
                <img
                  src="https://cloud.google.com/static/images/social-icon-google-cloud-1200-630.png"
                  alt="Google Cloud"
                  class="img-fluid rounded shadow"
                  style="max-height: 200px;"
                >
              </div>
            </div>

            <!-- Step 1: Enable APIs -->
            <div v-if="currentStep === 1" class="step">
              <h5 class="font-weight-bold mb-3">
                <i class="fas fa-toggle-on text-success me-2"></i>
                Enable Required APIs
              </h5>
              <div class="alert alert-warning">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Make sure your new project is selected in the project dropdown!
              </div>
              <ol class="setup-steps">
                <li class="mb-3">
                  Go to <a href="https://console.cloud.google.com/apis/library" target="_blank" class="text-primary">
                    <strong>APIs & Services > Library</strong>
                    <i class="fas fa-external-link-alt ms-1 small"></i>
                  </a>
                </li>
                <li class="mb-3">
                  Search for and enable these APIs:
                  <div class="mt-2">
                    <span class="badge bg-gradient-primary me-2 mb-2">Gmail API</span>
                    <span class="badge bg-gradient-info me-2 mb-2">Google Sheets API</span>
                    <span class="badge bg-gradient-success me-2 mb-2">Google Drive API</span>
                  </div>
                </li>
                <li class="mb-3">
                  For each API:
                  <ul class="mt-2">
                    <li>Click on the API name</li>
                    <li>Click the blue <strong>"Enable"</strong> button</li>
                    <li>Wait for it to activate (takes a few seconds)</li>
                  </ul>
                </li>
              </ol>
            </div>

            <!-- Step 2: Configure OAuth Consent Screen -->
            <div v-if="currentStep === 2" class="step">
              <h5 class="font-weight-bold mb-3">
                <i class="fas fa-shield-alt text-warning me-2"></i>
                Configure OAuth Consent Screen
              </h5>
              <ol class="setup-steps">
                <li class="mb-3">
                  Go to <a href="https://console.cloud.google.com/apis/credentials/consent" target="_blank" class="text-primary">
                    <strong>APIs & Services > OAuth consent screen</strong>
                    <i class="fas fa-external-link-alt ms-1 small"></i>
                  </a>
                </li>
                <li class="mb-3">
                  Select <strong>"External"</strong> user type
                  <br><small class="text-muted">This allows you to use any Google account for testing</small>
                </li>
                <li class="mb-3">
                  Click <strong>"Create"</strong>
                </li>
                <li class="mb-3">
                  Fill in the required fields:
                  <div class="card mt-2 bg-light">
                    <div class="card-body">
                      <div class="mb-2"><strong>App name:</strong> Lodgeick</div>
                      <div class="mb-2"><strong>User support email:</strong> Your email</div>
                      <div class="mb-2"><strong>Developer contact:</strong> Your email</div>
                    </div>
                  </div>
                </li>
                <li class="mb-3">
                  Click <strong>"Save and Continue"</strong>
                </li>
                <li class="mb-3">
                  On the "Scopes" page, click <strong>"Add or Remove Scopes"</strong>
                </li>
                <li class="mb-3">
                  Search for and select these scopes:
                  <div class="card mt-2 bg-light">
                    <div class="card-body small">
                      <div class="mb-1"><code>https://www.googleapis.com/auth/gmail.readonly</code></div>
                      <div class="mb-1"><code>https://www.googleapis.com/auth/gmail.send</code></div>
                      <div class="mb-1"><code>https://www.googleapis.com/auth/spreadsheets</code></div>
                      <div class="mb-1"><code>https://www.googleapis.com/auth/drive.file</code></div>
                    </div>
                  </div>
                </li>
                <li class="mb-3">
                  Click <strong>"Update"</strong> then <strong>"Save and Continue"</strong>
                </li>
                <li class="mb-3">
                  On the "Test users" page, click <strong>"Add Users"</strong>
                </li>
                <li class="mb-3">
                  Add your Gmail address (the one you'll test with)
                </li>
                <li class="mb-3">
                  Click <strong>"Save and Continue"</strong> through the remaining steps
                </li>
              </ol>
            </div>

            <!-- Step 3: Create OAuth Credentials -->
            <div v-if="currentStep === 3" class="step">
              <h5 class="font-weight-bold mb-3">
                <i class="fas fa-key text-danger me-2"></i>
                Create OAuth 2.0 Credentials
              </h5>
              <ol class="setup-steps">
                <li class="mb-3">
                  Go to <a href="https://console.cloud.google.com/apis/credentials" target="_blank" class="text-primary">
                    <strong>APIs & Services > Credentials</strong>
                    <i class="fas fa-external-link-alt ms-1 small"></i>
                  </a>
                </li>
                <li class="mb-3">
                  Click <strong>"Create Credentials"</strong> at the top
                </li>
                <li class="mb-3">
                  Select <strong>"OAuth 2.0 Client ID"</strong>
                </li>
                <li class="mb-3">
                  Application type: <strong>"Web application"</strong>
                </li>
                <li class="mb-3">
                  Name: <strong>"Lodgeick Local"</strong> (or any name you prefer)
                </li>
                <li class="mb-3">
                  Under <strong>"Authorized redirect URIs"</strong>, click <strong>"Add URI"</strong>
                </li>
                <li class="mb-3">
                  Add this exact URI:
                  <div class="input-group mt-2">
                    <input
                      type="text"
                      class="form-control"
                      :value="redirectUri"
                      readonly
                    >
                    <button
                      class="btn btn-outline-secondary"
                      @click="copyToClipboard(redirectUri)"
                    >
                      <i class="fas fa-copy"></i>
                    </button>
                  </div>
                  <small class="text-muted">Click the copy button to copy the URI</small>
                </li>
                <li class="mb-3">
                  Click <strong>"Create"</strong>
                </li>
                <li class="mb-3">
                  A dialog will appear showing your credentials
                  <div class="alert alert-warning mt-2">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    <strong>Important:</strong> Copy both the Client ID and Client Secret - you'll need them in the next step!
                  </div>
                </li>
              </ol>
            </div>

            <!-- Step 4: Configure Lodgeick -->
            <div v-if="currentStep === 4" class="step">
              <h5 class="font-weight-bold mb-3">
                <i class="fas fa-cog text-info me-2"></i>
                Configure Lodgeick
              </h5>
              <p>Enter your OAuth credentials from Google Cloud Console:</p>

              <div class="mb-3">
                <label class="form-label font-weight-bold">
                  Client ID
                  <span class="text-danger">*</span>
                </label>
                <input
                  v-model="clientId"
                  type="text"
                  class="form-control"
                  placeholder="1234567890-abc123def456.apps.googleusercontent.com"
                >
                <small class="text-muted">
                  Ends with .apps.googleusercontent.com
                </small>
              </div>

              <div class="mb-3">
                <label class="form-label font-weight-bold">
                  Client Secret
                  <span class="text-danger">*</span>
                </label>
                <div class="input-group">
                  <input
                    v-model="clientSecret"
                    :type="showSecret ? 'text' : 'password'"
                    class="form-control"
                    placeholder="GOCSPX-xxxxxxxxxxxxx"
                  >
                  <button
                    class="btn btn-outline-secondary"
                    @click="showSecret = !showSecret"
                  >
                    <i :class="showSecret ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                  </button>
                </div>
                <small class="text-muted">
                  Usually starts with GOCSPX-
                </small>
              </div>

              <div class="alert alert-success" v-if="clientId && clientSecret">
                <i class="fas fa-check-circle me-2"></i>
                Credentials look good! Click "Save & Test Connection" to finish.
              </div>
            </div>

            <!-- Step 5: Complete -->
            <div v-if="currentStep === 5" class="step text-center">
              <div class="icon icon-shape bg-gradient-success shadow-success mx-auto mb-4" style="width: 80px; height: 80px;">
                <i class="fas fa-check text-white" style="font-size: 2.5rem;"></i>
              </div>
              <h4 class="font-weight-bold mb-3">Setup Complete!</h4>
              <p class="text-muted mb-4">
                Your OAuth credentials have been configured successfully.
              </p>
              <div class="alert alert-info">
                <i class="fas fa-lightbulb me-2"></i>
                You can now close this wizard and click "Connect App" to authenticate with {{ providerName }}.
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="modal-footer">
          <button
            v-if="currentStep > 0 && currentStep < 5"
            type="button"
            class="btn btn-secondary"
            @click="previousStep"
          >
            <i class="fas fa-arrow-left me-2"></i>
            Previous
          </button>
          <button
            v-if="currentStep < 4"
            type="button"
            class="btn btn-primary"
            @click="nextStep"
          >
            Next
            <i class="fas fa-arrow-right ms-2"></i>
          </button>
          <button
            v-if="currentStep === 4"
            type="button"
            class="btn btn-success"
            @click="saveCredentials"
            :disabled="!clientId || !clientSecret || saving"
          >
            <span v-if="saving">
              <span class="spinner-border spinner-border-sm me-2"></span>
              Saving...
            </span>
            <span v-else>
              <i class="fas fa-save me-2"></i>
              Save & Test Connection
            </span>
          </button>
          <button
            v-if="currentStep === 5"
            type="button"
            class="btn btn-primary"
            @click="closeWizard"
          >
            <i class="fas fa-check me-2"></i>
            Done
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { createResource } from "frappe-ui"

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  provider: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close', 'success'])

const currentStep = ref(0)
const clientId = ref('')
const clientSecret = ref('')
const showSecret = ref(false)
const saving = ref(false)

const providerName = computed(() => {
  const names = {
    google: 'Google (Gmail, Sheets, Drive)',
    xero: 'Xero',
    slack: 'Slack'
  }
  return names[props.provider] || props.provider
})

const redirectUri = computed(() => {
  return window.location.origin + '/oauth/callback'
})

const steps = [
  { title: 'Create Project' },
  { title: 'Enable APIs' },
  { title: 'Consent Screen' },
  { title: 'Create Credentials' },
  { title: 'Configure' },
  { title: 'Complete' }
]

// Save credentials resource
const saveCredentialsResource = createResource({
  url: "lodgeick.api.oauth.save_oauth_credentials",
  makeParams() {
    return {
      provider: props.provider,
      client_id: clientId.value,
      client_secret: clientSecret.value
    }
  },
  onSuccess() {
    saving.value = false
    currentStep.value = 5
    emit('success', {
      provider: props.provider,
      client_id: clientId.value,
      client_secret: clientSecret.value
    })
  },
  onError(error) {
    saving.value = false
    alert(`Failed to save credentials: ${error.message || error}`)
  }
})

function nextStep() {
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  }
}

function previousStep() {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

function saveCredentials() {
  if (!clientId.value || !clientSecret.value) {
    alert('Please enter both Client ID and Client Secret')
    return
  }

  saving.value = true
  saveCredentialsResource.submit()
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    // Show toast or temporary message
    const button = event.target.closest('button')
    const icon = button.querySelector('i')
    icon.className = 'fas fa-check'
    setTimeout(() => {
      icon.className = 'fas fa-copy'
    }, 2000)
  })
}

function closeWizard() {
  currentStep.value = 0
  clientId.value = ''
  clientSecret.value = ''
  showSecret.value = false
  emit('close')
}
</script>

<style scoped>
.step-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #e9ecef;
  color: #6c757d;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  transition: all 0.3s ease;
}

.step-circle.active {
  background: linear-gradient(310deg, #7928CA 0%, #FF0080 100%);
  color: white;
  box-shadow: 0 4px 20px 0 rgba(121, 40, 202, 0.4);
}

.step-circle.completed {
  background: linear-gradient(310deg, #17AD37 0%, #98EC2D 100%);
  color: white;
}

.step-line {
  position: absolute;
  top: 24px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: #e9ecef;
  z-index: -1;
  transition: all 0.3s ease;
}

.step-line.completed {
  background: linear-gradient(310deg, #17AD37 0%, #98EC2D 100%);
}

.setup-steps {
  padding-left: 1.5rem;
}

.setup-steps li {
  line-height: 1.8;
}

.bg-gradient-primary {
  background: linear-gradient(310deg, #7928CA 0%, #FF0080 100%);
}

.bg-gradient-success {
  background: linear-gradient(310deg, #17AD37 0%, #98EC2D 100%);
}

.shadow-success {
  box-shadow: 0 4px 20px 0 rgba(23, 173, 55, 0.4) !important;
}

.icon-shape {
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.font-weight-bold {
  font-weight: 700;
}

.modal.show {
  display: block;
}

.modal-dialog-scrollable .modal-body {
  max-height: calc(100vh - 200px);
  overflow-y: auto;
}
</style>
