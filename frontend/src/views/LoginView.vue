<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <i class="pi pi-comments login-icon"></i>
        <h2>Welcome Back 👋</h2>
        <p>Login to continue chatting</p>
      </div>

      <Message v-if="error" severity="error" :closable="false" class="error-msg">
        {{ error }}
      </Message>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <InputText
            id="username"
            v-model="username"
            placeholder="Enter your username"
            class="input"
            autocomplete="username"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <Password
            id="password"
            v-model="password"
            placeholder="••••••••"
            toggleMask
            :feedback="false"
            class="input"
            input-class="input"
            autocomplete="current-password"
            required
          />
        </div>

        <Button
          label="Login"
          icon="pi pi-sign-in"
          class="login-btn"
          :loading="loading"
          type="submit"
        />

        <p class="register-text">
          Don’t have an account?
          <router-link to="/register" class="register-link">Register</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../composables/useAuth";

// ✅ PrimeVue Components
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import Button from "primevue/button";
import Message from "primevue/message";

const { login } = useAuth();
const router = useRouter();

const username = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");

async function handleLogin() {
  loading.value = true;
  error.value = "";
  try {
    await login(username.value, password.value);
    router.push("/home");
  } catch (e) {
    error.value = "Invalid username or password.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped lang="scss">
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--surface-ground);
}

.login-card {
  background: var(--surface-card);
  padding: 2.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 420px;
}

.login-header {
  text-align: center;
  margin-bottom: 1.5rem;

  h2 {
    margin-bottom: 0.25rem;
    color: var(--text-color);
  }

  p {
    color: var(--text-color-secondary);
    font-size: 0.95rem;
  }

  .login-icon {
    font-size: 2.2rem;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
  }
}

.form-group {
  margin-bottom: 1rem;

  label {
    display: block;
    font-weight: 600;
    margin-bottom: 0.4rem;
    color: var(--text-color);
  }

  .input {
    width: 100%;
  }
}

.login-btn {
  width: 100%;
  margin-top: 0.5rem;
}

.register-text {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.9rem;
  color: var(--text-color-secondary);

  .register-link {
    color: var(--primary-color);
    font-weight: 600;
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
}

.error-msg {
  margin-bottom: 1rem;
}
</style>
