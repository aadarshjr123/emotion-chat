<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <i class="pi pi-user-plus register-icon"></i>
        <h2>Create Account ✨</h2>
        <p>Join and start chatting instantly</p>
      </div>

      <Message v-if="error" severity="error" :closable="false" class="error-msg">
        {{ error }}
      </Message>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">Username</label>
          <InputText
            id="username"
            v-model="username"
            placeholder="Choose a username"
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
            placeholder="Create a password"
            toggleMask
            :feedback="false"
            class="input"
            input-class="input"
            autocomplete="new-password"
            required
          />
        </div>

        <Button
          label="Register"
          icon="pi pi-check"
          class="register-btn"
          :loading="loading"
          type="submit"
        />

        <p class="login-text">
          Already have an account?
          <router-link to="/login" class="login-link">Login</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../composables/useAuth";

// ✅ PrimeVue components
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import Button from "primevue/button";
import Message from "primevue/message";

const router = useRouter();
const { register } = useAuth();

const username = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

async function handleRegister() {
  loading.value = true;
  error.value = "";
  try {
    await register(username.value, password.value);
    router.push("/home");
  } catch (err: any) {
    error.value = err.response?.data?.detail || "Registration failed";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped lang="scss">
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--surface-ground);
}

.register-card {
  background: var(--surface-card);
  padding: 2.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 420px;
}

.register-header {
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

  .register-icon {
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

.register-btn {
  width: 100%;
  margin-top: 0.5rem;
}

.login-text {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.9rem;
  color: var(--text-color-secondary);

  .login-link {
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
