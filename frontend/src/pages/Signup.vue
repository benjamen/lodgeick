<template>
  <div class="auth-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-5 col-md-7">
          <div class="card shadow-lg border-0 mt-5">
            <div class="card-header bg-gradient-primary p-4 text-center">
              <h3 class="text-white font-weight-bold mb-0">Create Your Account</h3>
              <p class="text-white opacity-8 mb-0 mt-2">Start connecting your apps today</p>
            </div>
            <div class="card-body p-4">
              <form @submit.prevent="handleSignup">
                <div class="mb-3">
                  <label class="form-label font-weight-bold">Full Name</label>
                  <input
                    v-model="formData.fullName"
                    type="text"
                    class="form-control"
                    placeholder="John Doe"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label font-weight-bold">Email Address</label>
                  <input
                    v-model="formData.email"
                    type="email"
                    class="form-control"
                    placeholder="john@example.com"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label font-weight-bold">Password</label>
                  <input
                    v-model="formData.password"
                    type="password"
                    class="form-control"
                    placeholder="••••••••"
                    required
                    minlength="6"
                  />
                  <small class="text-muted">Minimum 6 characters</small>
                </div>

                <div v-if="error" class="alert alert-danger">
                  {{ error }}
                </div>

                <button
                  type="submit"
                  class="btn btn-primary w-100 mb-3"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ loading ? 'Creating Account...' : 'Create Account' }}
                </button>

                <div class="text-center">
                  <p class="text-muted mb-0">
                    Already have an account?
                    <router-link to="/account/login" class="text-primary font-weight-bold">
                      Sign In
                    </router-link>
                  </p>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { createResource } from "frappe-ui"

const router = useRouter()

const formData = ref({
  fullName: "",
  email: "",
  password: ""
})

const error = ref("")
const loading = ref(false)

const signupResource = createResource({
  url: "frappe.core.doctype.user.user.sign_up",
  makeParams(values) {
    return {
      email: values.email,
      full_name: values.fullName,
      redirect_to: "/frontend"
    }
  },
  onSuccess(data) {
    loading.value = false
    if (data.message === "Please check your email for verification") {
      alert("Account created successfully! Please check your email to verify your account.")
      router.push("/account/login")
    } else {
      // Auto-login successful
      router.push("/")
    }
  },
  onError(err) {
    loading.value = false
    error.value = err.messages ? err.messages.join(", ") : err.message || "Failed to create account"
  }
})

function handleSignup() {
  error.value = ""
  loading.value = true

  signupResource.submit({
    email: formData.value.email,
    fullName: formData.value.fullName
  })
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: linear-gradient(310deg, #141727 0%, #3A416F 100%);
  display: flex;
  align-items: center;
  padding: 2rem 0;
}

.bg-gradient-primary {
  background: linear-gradient(310deg, #7928CA 0%, #FF0080 100%);
}

.card {
  border-radius: 1rem;
}

.card-header {
  border-radius: 1rem 1rem 0 0 !important;
}

.form-control {
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  border: 1px solid #d2d6da;
}

.form-control:focus {
  border-color: #7928CA;
  box-shadow: 0 0 0 0.2rem rgba(121, 40, 202, 0.25);
}

.btn-primary {
  background: linear-gradient(310deg, #7928CA 0%, #FF0080 100%);
  border: none;
  border-radius: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(121, 40, 202, 0.4);
}

.font-weight-bold {
  font-weight: 700;
}
</style>
