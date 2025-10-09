<template>
  <div class="auth-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-5 col-md-7">
          <div class="card shadow-lg border-0 mt-5">
            <div class="card-header bg-gradient-primary p-4 text-center">
              <h3 class="text-white font-weight-bold mb-0">Welcome Back</h3>
              <p class="text-white opacity-8 mb-0 mt-2">Sign in to connect your apps</p>
            </div>
            <div class="card-body p-4">
              <form @submit.prevent="submit">
                <div class="mb-3">
                  <label class="form-label font-weight-bold">Email or Username</label>
                  <input
                    name="email"
                    type="text"
                    class="form-control"
                    placeholder="john@example.com or Administrator"
                    required
                  />
                  <small class="text-muted">You can log in with your email address or username</small>
                </div>
                <div class="mb-3">
                  <label class="form-label font-weight-bold">Password</label>
                  <input
                    name="password"
                    type="password"
                    class="form-control"
                    placeholder="••••••••"
                    required
                  />
                </div>

                <button
                  type="submit"
                  class="btn btn-primary w-100 mb-3"
                  :disabled="session.login.loading"
                >
                  <span v-if="session.login.loading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ session.login.loading ? 'Signing In...' : 'Sign In' }}
                </button>

                <div class="text-center">
                  <p class="text-muted mb-2">
                    Don't have an account?
                    <router-link to="/account/signup" class="text-primary font-weight-bold">
                      Create Account
                    </router-link>
                  </p>
                  <p class="text-muted mb-0">
                    <a href="/desk" class="text-muted text-decoration-none">
                      <small>Administrator? Access Frappe Desk →</small>
                    </a>
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

<script lang="ts" setup>
import { session } from "../data/session"

function submit(e) {
	const formData = new FormData(e.target)
	session.login.submit({
		email: formData.get("email"),
		password: formData.get("password"),
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
