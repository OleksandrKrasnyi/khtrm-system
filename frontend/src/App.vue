<template>
  <div id="app">
    <!-- Global notifications -->
    <GlobalNotifications />

    <!-- Main container -->
    <div class="app-container">
      <!-- Header for non-authenticated users -->
      <header v-if="!isAuthenticated" class="app-header">
        <div class="container">
          <h1 class="app-title">
            <i class="fas fa-bus" />
            KHTRM - Система управління транспортом
          </h1>
          <p class="app-subtitle">м. Харків</p>
        </div>
      </header>

      <!-- Navigation bar for authenticated users -->
      <nav v-if="isAuthenticated" class="app-nav">
        <div class="container">
          <div class="nav-brand">
            <i class="fas fa-bus" />
            <span>KHTRM</span>
          </div>

          <div class="nav-menu">
            <router-link to="/dashboard" class="nav-link">
              <i class="fas fa-tachometer-alt" />
              Головна
            </router-link>

            <!-- Simple user info and logout -->
            <div v-if="userRole" class="nav-user">
              <span class="user-role">{{ userRole.display_name_uk }}</span>
              <button class="logout-btn" @click="logout">
                <i class="fas fa-sign-out-alt" />
                Вихід
              </button>
            </div>
          </div>
        </div>
      </nav>

      <!-- Main content -->
      <main class="app-main">
        <div class="container">
          <router-view />
        </div>
      </main>

      <!-- Footer -->
      <footer class="app-footer">
        <div class="container">
          <p>&copy; 2025 KHTRM - Система управління транспортом м. Харків</p>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import GlobalNotifications from "./components/GlobalNotifications.vue";
import { useAuth } from "./composables/useAuth";
import { useNotifications } from "./composables/useNotifications";

const router = useRouter();
const { isAuthenticated, userRole, logout: authLogout } = useAuth();
const { showSuccess } = useNotifications();

// Check authentication on app mount
onMounted(async () => {
  // If user is not authenticated and not on login page, redirect to login
  if (!isAuthenticated.value && router.currentRoute.value.path !== "/login") {
    await router.push("/login");
  }
});

// Handle logout
const logout = async (): Promise<void> => {
  try {
    await authLogout();
    showSuccess("Ви успішно вийшли з системи");
    router.push("/login");
  } catch (error) {
    console.error("Logout error:", error);
  }
};
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  color: white;
  padding: 2rem 0;
  text-align: center;
}

.app-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.app-subtitle {
  font-size: 1.2rem;
  margin: 0.5rem 0 0;
  opacity: 0.9;
}

.app-nav {
  background: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.app-nav .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.5rem;
  font-weight: 700;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 1rem;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.router-link-active {
  background-color: #3498db;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-role {
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
}

.logout-btn {
  background: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
  border: 1px solid #e74c3c;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logout-btn:hover {
  background: #e74c3c;
  color: white;
}

.app-main {
  flex: 1;
  padding: 2rem 0;
}

.app-footer {
  background: #34495e;
  color: white;
  text-align: center;
  padding: 1rem 0;
  margin-top: auto;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}
</style>
