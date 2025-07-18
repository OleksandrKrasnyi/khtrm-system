<template>
  <div class="admin-dashboard">
    <div class="admin-header">
      <h1>
        <i class="fas fa-user-shield" />
        Панель адміністратора
      </h1>
      <p class="admin-subtitle">Управління системою та моніторинг</p>
    </div>

    <div class="admin-navigation">
      <nav class="admin-nav">
        <button
          v-for="section in sections"
          :key="section.id"
          :class="['nav-btn', { active: activeSection === section.id }]"
          @click="activeSection = section.id"
        >
          <i :class="section.icon" />
          <span>{{ section.name }}</span>
        </button>
      </nav>
    </div>

    <div class="admin-content">
      <!-- Overview Section -->
      <div v-if="activeSection === 'overview'" class="overview-section">
        <div class="welcome-card">
          <h2>
            <i class="fas fa-tachometer-alt" />
            Огляд системи
          </h2>
          <p>Ласкаво просимо до панелі адміністратора KHTRM системи!</p>
        </div>

        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-database" />
            </div>
            <div class="stat-info">
              <h3>{{ availableDatabases.length }}</h3>
              <p>Баз даних</p>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-table" />
            </div>
            <div class="stat-info">
              <h3>{{ totalTables }}</h3>
              <p>Таблиць</p>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-users" />
            </div>
            <div class="stat-info">
              <h3>{{ profilesCount }}</h3>
              <p>Профілів користувачів</p>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-cogs" />
            </div>
            <div class="stat-info">
              <h3>{{ configuredTables }}</h3>
              <p>Налаштованих таблиць</p>
            </div>
          </div>
        </div>

        <div class="quick-actions">
          <h3>Швидкі дії</h3>
          <div class="actions-grid">
            <button class="action-btn" @click="activeSection = 'database'">
              <i class="fas fa-database" />
              <span>Моніторинг БД</span>
            </button>
            <button class="action-btn" @click="activeSection = 'fields'">
              <i class="fas fa-cogs" />
              <span>Налаштування полів</span>
            </button>
            <button class="action-btn" @click="activeSection = 'constructor'">
              <i class="fas fa-table" />
              <span>Конструктор таблиць</span>
            </button>
            <button class="action-btn" @click="activeSection = 'users'">
              <i class="fas fa-users" />
              <span>Користувачі</span>
            </button>
            <button class="action-btn" @click="activeSection = 'system'">
              <i class="fas fa-server" />
              <span>Системні настройки</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Database Monitor Section -->
      <div v-if="activeSection === 'database'" class="section-content">
        <DatabaseMonitor />
      </div>

      <!-- Field Settings Section -->
      <div v-if="activeSection === 'fields'" class="section-content">
        <AdminFieldSettings />
      </div>

      <!-- Table Constructor Section -->
      <div v-if="activeSection === 'constructor'" class="section-content">
        <TableConstructor />
      </div>

      <!-- Users Section -->
      <div v-if="activeSection === 'users'" class="section-content">
        <UserManagement />
      </div>

      <!-- System Settings Section -->
      <div v-if="activeSection === 'system'" class="section-content">
        <SystemSettings />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, defineAsyncComponent } from "vue";
import { useNotifications } from "@/composables/useNotifications";

// Use defineAsyncComponent for better performance
const DatabaseMonitor = defineAsyncComponent(
  () => import("./DatabaseMonitor.vue"),
);
const AdminFieldSettings = defineAsyncComponent(
  () => import("./AdminFieldSettings.vue"),
);
const TableConstructor = defineAsyncComponent(
  () => import("./TableConstructor.vue"),
);
const UserManagement = defineAsyncComponent(
  () => import("./UserManagement.vue"),
);
const SystemSettings = defineAsyncComponent(
  () => import("./SystemSettings.vue"),
);

const { addNotification } = useNotifications();

// Navigation state
const activeSection = ref<string>("overview");

// Navigation sections
const sections = [
  {
    id: "overview",
    name: "Огляд",
    icon: "fas fa-tachometer-alt",
  },
  {
    id: "database",
    name: "Моніторинг БД",
    icon: "fas fa-database",
  },
  {
    id: "fields",
    name: "Поля",
    icon: "fas fa-cogs",
  },
  {
    id: "constructor",
    name: "Конструктор таблиць",
    icon: "fas fa-table",
  },
  {
    id: "users",
    name: "Користувачі",
    icon: "fas fa-users",
  },
  {
    id: "system",
    name: "Система",
    icon: "fas fa-server",
  },
];

// Statistics data
const availableDatabases = ref<string[]>([]);
const totalTables = ref<number>(0);
const profilesCount = ref<number>(5); // Known profiles count
const configuredTables = ref<number>(0);

// Computed properties
const hasConfiguredTables = computed(() => {
  const savedConfigs = Object.keys(localStorage).filter((key) =>
    key.startsWith("khtrm-admin-field-configs-"),
  );
  return savedConfigs.length;
});

// Methods
const loadSystemStats = async () => {
  try {
    // Load databases
    const dbResponse = await fetch(
      "http://localhost:8000/api/dispatcher/admin/databases",
    );
    if (dbResponse.ok) {
      const dbData = await dbResponse.json();
      availableDatabases.value = dbData.databases;

      // Load total tables count for all databases
      let tablesCount = 0;
      for (const db of dbData.databases) {
        try {
          const tablesResponse = await fetch(
            `http://localhost:8000/api/dispatcher/admin/tables?database_name=${db}`,
          );
          if (tablesResponse.ok) {
            const tablesData = await tablesResponse.json();
            tablesCount += tablesData.tables.length;
          }
        } catch (error) {
          console.error(`Error loading tables for ${db}:`, error);
        }
      }
      totalTables.value = tablesCount;
    }

    // Count configured tables
    configuredTables.value = hasConfiguredTables.value;
  } catch (error) {
    console.error("Error loading system statistics:", error);
    addNotification({
      type: "error",
      message: "Помилка завантаження статистики системи",
    });
  }
};

// Initialize
onMounted(() => {
  loadSystemStats();
});
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: #f8f9fa;
}

.admin-header {
  background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  color: white;
  padding: 30px;
  text-align: center;
}

.admin-header h1 {
  margin: 0 0 10px 0;
  font-size: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.admin-subtitle {
  margin: 0;
  font-size: 1.2rem;
  opacity: 0.9;
}

.admin-navigation {
  background: white;
  border-bottom: 2px solid #e1e8ed;
  padding: 0 15px;
}

.admin-nav {
  display: flex;
  gap: 0;
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
  justify-content: space-between;
}

.admin-nav::-webkit-scrollbar {
  display: none;
}

.nav-btn {
  background: none;
  border: none;
  padding: 16px 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #7f8c8d;
  transition: all 0.3s;
  border-bottom: 3px solid transparent;
  white-space: nowrap;
  flex: 1;
  min-width: 0;
  text-align: center;
  justify-content: center;
}

.nav-btn:hover {
  color: #3498db;
  background: rgba(52, 152, 219, 0.1);
}

.nav-btn.active {
  color: #3498db;
  border-bottom-color: #3498db;
  background: rgba(52, 152, 219, 0.1);
}

.nav-btn i {
  font-size: 1.2rem;
}

.admin-content {
  padding: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.overview-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.welcome-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.welcome-card h2 {
  color: #2c3e50;
  margin: 0 0 15px 0;
  font-size: 1.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.welcome-card p {
  color: #7f8c8d;
  margin: 0;
  font-size: 1.1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 20px;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-info h3 {
  margin: 0 0 5px 0;
  font-size: 2rem;
  color: #2c3e50;
  font-weight: 700;
}

.stat-info p {
  margin: 0;
  color: #7f8c8d;
  font-size: 1rem;
}

.quick-actions {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.quick-actions h3 {
  color: #2c3e50;
  margin: 0 0 20px 0;
  font-size: 1.5rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.action-btn {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  border: none;
  padding: 20px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s;
}

.action-btn:hover {
  background: linear-gradient(135deg, #2980b9, #1f5f8b);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.action-btn i {
  font-size: 1.2rem;
}

.section-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* Responsive design */
@media (max-width: 768px) {
  .admin-header {
    padding: 20px 15px;
  }

  .admin-header h1 {
    font-size: 2rem;
  }

  .admin-navigation {
    padding: 0 15px;
  }

  .admin-content {
    padding: 20px 15px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 20px;
  }

  .stat-info h3 {
    font-size: 1.5rem;
  }
}

/* Custom scrollbar for navigation */
@media (max-width: 768px) {
  .admin-nav {
    padding-bottom: 10px;
  }

  .nav-btn {
    padding: 12px 8px;
    font-size: 0.8rem;
    gap: 4px;
  }

  .nav-btn i {
    font-size: 1rem;
  }

  .admin-nav::-webkit-scrollbar {
    display: block;
    height: 4px;
  }

  .admin-nav::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 2px;
  }

  .admin-nav::-webkit-scrollbar-thumb {
    background: #3498db;
    border-radius: 2px;
  }

  .admin-nav::-webkit-scrollbar-thumb:hover {
    background: #2980b9;
  }
}

/* Extra small screens */
@media (max-width: 480px) {
  .nav-btn {
    padding: 10px 6px;
    font-size: 0.75rem;
    gap: 3px;
  }

  .nav-btn i {
    font-size: 0.9rem;
  }

  .admin-navigation {
    padding: 0 5px;
  }
}
</style>
