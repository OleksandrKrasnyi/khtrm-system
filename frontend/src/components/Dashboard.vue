<template>
  <div class="dashboard">
    <!-- Для админа показываем новую панель управления -->
    <AdminDashboard v-if="isAdmin" />

    <!-- Для нарядчика показываем таблицу нарядов -->
    <AssignmentTable v-else-if="isDispatcher" />

    <!-- Для остальных ролей показываем приветствие -->
    <div v-else class="welcome-section">
      <div class="welcome-icon">
        <i class="fas fa-user-circle" />
      </div>
      <h1>Привіт, {{ userRole?.display_name_uk }}!</h1>
      <p class="welcome-subtitle">Ласкаво просимо до системи KHTRM</p>
      <div class="user-info">
        <p><strong>Користувач:</strong> {{ user?.username }}</p>
        <p><strong>Email:</strong> {{ user?.email }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, defineAsyncComponent } from "vue";
import { useAuth } from "../composables/useAuth";

// Use defineAsyncComponent for better performance
const AssignmentTable = defineAsyncComponent(
  () => import("./AssignmentTable.vue"),
);
const AdminDashboard = defineAsyncComponent(
  () => import("./AdminDashboard.vue"),
);

const { user, userRole } = useAuth();

// Check if current user is an admin
const isAdmin = computed(() => {
  return userRole.value?.name === "super_admin";
});

// Check if current user is a dispatcher
const isDispatcher = computed(() => {
  return userRole.value?.name === "dispatcher";
});
</script>

<style scoped>
.dashboard {
  padding: 1rem;
  min-height: 50vh;
}

/* For dispatcher table - full width */
.dashboard:has(> .assignment-table) {
  padding: 0;
}

/* For welcome section - centered */
.dashboard:has(> .welcome-section) {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.welcome-section {
  text-align: center;
  background: white;
  padding: 3rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  width: 100%;
}

.welcome-icon {
  font-size: 4rem;
  color: #3498db;
  margin-bottom: 1.5rem;
}

.welcome-section h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin: 0 0 1rem;
  font-weight: 700;
}

.welcome-subtitle {
  font-size: 1.2rem;
  color: #7f8c8d;
  margin: 0 0 2rem;
}

.user-info {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 12px;
  border-left: 4px solid #3498db;
  text-align: left;
}

.user-info p {
  margin: 0.5rem 0;
  color: #2c3e50;
  font-size: 1rem;
}

.user-info strong {
  color: #3498db;
}

@media (max-width: 768px) {
  .welcome-section {
    padding: 2rem;
  }

  .welcome-section h1 {
    font-size: 2rem;
  }

  .welcome-icon {
    font-size: 3rem;
  }
}
</style>
