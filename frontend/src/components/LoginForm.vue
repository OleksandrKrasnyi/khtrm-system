<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h2>Вхід до системи</h2>
        <p>KHTRM - Система управління транспортом</p>
      </div>

      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Користувач:</label>
          <input
            id="username"
            v-model="credentials.username"
            type="text"
            required
            class="form-input"
            placeholder="Введіть логін"
          />
        </div>

        <div class="form-group">
          <label for="password">Пароль:</label>
          <input
            id="password"
            v-model="credentials.password"
            type="password"
            required
            class="form-input"
            placeholder="Введіть пароль"
          />
        </div>

        <button type="submit" :disabled="isLoading" class="login-btn">
          <i v-if="isLoading" class="fas fa-spinner fa-spin" />
          {{ isLoading ? "Входження..." : "Увійти" }}
        </button>
      </form>

      <div class="login-info">
        <p><strong>Тестові користувачі:</strong></p>
        <div class="test-users">
          <div class="user-item"><strong>nar</strong> / nar - Нарядчик</div>
          <div class="user-item">
            <strong>taba</strong> / taba - Табельник A
          </div>
          <div class="user-item">
            <strong>tabb</strong> / tabb - Табельник B
          </div>
          <div class="user-item"><strong>dys</strong> / dys - Диспетчер</div>
          <div class="user-item">
            <strong>buc</strong> / buc - Бухгалтер з палива
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../composables/useAuth";
import { useNotifications } from "../composables/useNotifications";
import type { LoginCredentials } from "@/types";

const router = useRouter();
const { login } = useAuth();
const { showSuccess, showError } = useNotifications();

const isLoading = ref<boolean>(false);
const credentials = ref<LoginCredentials>({
  username: "",
  password: "",
});

const handleLogin = async (): Promise<void> => {
  if (!credentials.value.username || !credentials.value.password) {
    showError("Будь ласка, заповніть всі поля");
    return;
  }

  isLoading.value = true;

  try {
    await login(credentials.value);
    showSuccess("Успішний вхід до системи!");
    router.push("/dashboard");
  } catch (error) {
    console.error("Login error:", error);
    showError("Помилка входу. Перевірте логін та пароль.");
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
}

.login-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h2 {
  color: #2c3e50;
  margin: 0 0 0.5rem;
  font-size: 1.8rem;
  font-weight: 700;
}

.login-header p {
  color: #7f8c8d;
  margin: 0;
  font-size: 0.9rem;
}

.login-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 600;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
}

.login-btn {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(52, 152, 219, 0.3);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.login-info {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  border-left: 4px solid #3498db;
}

.login-info p {
  margin: 0 0 0.5rem;
  font-size: 0.9rem;
  color: #495057;
}

.test-users {
  background: white;
  padding: 0.75rem;
  border-radius: 4px;
  border: 1px solid #dee2e6;
}

.user-item {
  padding: 0.25rem 0;
  font-family: monospace;
  font-size: 0.85rem;
  color: #495057;
  border-bottom: 1px solid #f8f9fa;
}

.user-item:last-child {
  border-bottom: none;
}

.user-item strong {
  color: #3498db;
}
</style>
