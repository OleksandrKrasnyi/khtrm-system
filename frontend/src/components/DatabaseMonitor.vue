<template>
  <div class="database-monitor">
    <div class="monitor-header">
      <h1>
        <i class="fas fa-database" />
        Моніторинг структури БД
      </h1>
      <p class="monitor-subtitle">
        Перегляд структури баз даних, таблиць та полів
      </p>
    </div>

    <div class="monitor-controls">
      <div class="database-selector">
        <label>База даних:</label>
        <select
          v-model="selectedDatabase"
          class="database-select"
          @change="loadTables"
        >
          <option v-for="db in availableDatabases" :key="db" :value="db">
            {{ db }}
          </option>
        </select>
      </div>

      <div class="table-selector">
        <label>Таблиця:</label>
        <select
          v-model="selectedTable"
          class="table-select"
          @change="loadTableFields"
        >
          <option value="">Виберіть таблицю...</option>
          <option
            v-for="table in availableTables"
            :key="table.name"
            :value="table.name"
          >
            {{ table.name }} ({{ table.row_count }} записів,
            {{ table.column_count }} стовпців)
          </option>
        </select>
      </div>

      <div v-if="loadingData" class="loading-indicator">
        <i class="fas fa-spinner fa-spin" />
        <span>Завантаження...</span>
      </div>
    </div>

    <div class="monitor-content">
      <!-- Database Overview -->
      <div v-if="selectedDatabase && !selectedTable" class="database-overview">
        <h3>
          <i class="fas fa-table" />
          Таблиці в базі даних: {{ selectedDatabase }}
        </h3>

        <div class="tables-grid">
          <div
            v-for="table in availableTables"
            :key="table.name"
            class="table-card"
            @click="selectTable(table.name)"
          >
            <div class="table-header">
              <h4>{{ table.name }}</h4>
              <div class="table-stats">
                <span class="table-records">
                  <i class="fas fa-list-ol"></i>
                  {{ table.row_count }} записів
                </span>
                <span class="table-columns">
                  <i class="fas fa-columns"></i>
                  {{ table.column_count || 0 }} стовпців
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Table Structure -->
      <div
        v-if="selectedTable && tableFields.length > 0"
        class="table-structure"
      >
        <div class="structure-header">
          <h3>
            <i class="fas fa-columns" />
            Структура таблиці: {{ selectedTable }}
          </h3>
          <div class="structure-info">
            <span class="info-badge">{{ tableFields.length }} полів</span>
            <span class="info-badge">{{ selectedDatabase }}</span>
          </div>
        </div>

        <div class="fields-search">
          <input
            v-model="fieldSearch"
            type="text"
            placeholder="Пошук полів..."
            class="search-input"
          />
        </div>

        <div class="fields-table">
          <table class="table">
            <thead>
              <tr>
                <th>Назва поля</th>
                <th>Тип даних</th>
                <th>Null</th>
                <th>Ключ</th>
                <th>За замовчанням</th>
                <th>Приклади значень</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="field in filteredFields"
                :key="field.name"
                :class="{ 'key-field': field.is_key }"
              >
                <td class="field-name">
                  <i v-if="field.is_key" class="fas fa-key key-icon" />
                  {{ field.name }}
                </td>
                <td class="field-type">{{ field.type }}</td>
                <td class="field-nullable">
                  <span v-if="field.nullable" class="nullable-yes">YES</span>
                  <span v-else class="nullable-no">NO</span>
                </td>
                <td class="field-key">
                  <i v-if="field.is_key" class="fas fa-key" />
                </td>
                <td class="field-default">
                  {{ field.default_value || "-" }}
                </td>
                <td class="field-samples">
                  <div
                    v-if="field.sample_values && field.sample_values.length > 0"
                    class="samples"
                  >
                    <span
                      v-for="(sample, index) in field.sample_values"
                      :key="index"
                      class="sample-value"
                    >
                      {{ sample }}
                    </span>
                  </div>
                  <span v-else class="no-samples">-</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!selectedDatabase" class="empty-state">
        <i class="fas fa-database" />
        <h3>Виберіть базу даних</h3>
        <p>Оберіть базу даних зі списку вище для перегляду її структури</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import { useNotifications } from "@/composables/useNotifications";

const { addNotification } = useNotifications();

// Reactive state
const selectedDatabase = ref<string>("");
const selectedTable = ref<string>("");
const fieldSearch = ref<string>("");

// Database and table data
const availableDatabases = ref<string[]>([]);
const availableTables = ref<
  Array<{ name: string; row_count: number; column_count: number }>
>([]);
const tableFields = ref<
  Array<{
    name: string;
    type: string;
    nullable: boolean;
    is_key: boolean;
    default_value: string;
    sample_values: string[];
  }>
>([]);
const loadingData = ref<boolean>(false);

// Computed properties
const filteredFields = computed(() => {
  if (!fieldSearch.value) return tableFields.value;

  return tableFields.value.filter(
    (field) =>
      field.name.toLowerCase().includes(fieldSearch.value.toLowerCase()) ||
      field.type.toLowerCase().includes(fieldSearch.value.toLowerCase()),
  );
});

// Watchers
watch([selectedDatabase], () => {
  selectedTable.value = "";
  tableFields.value = [];
  fieldSearch.value = "";
});

watch([selectedTable], () => {
  fieldSearch.value = "";
});

// Methods
const selectTable = (tableName: string) => {
  selectedTable.value = tableName;
  loadTableFields();
};

// API functions
const loadDatabases = async () => {
  try {
    loadingData.value = true;
    const response = await fetch(
      "http://localhost:8000/api/dispatcher/admin/databases",
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    availableDatabases.value = data.databases;

    // Set default database if not already set
    if (!selectedDatabase.value && data.default_database) {
      selectedDatabase.value = data.default_database;
    }

    // Load tables for the selected database
    if (selectedDatabase.value) {
      await loadTables();
    }
  } catch (error) {
    addNotification({
      type: "error",
      message: "Помилка завантаження баз даних",
    });
  } finally {
    loadingData.value = false;
  }
};

const loadTables = async () => {
  if (!selectedDatabase.value) return;

  try {
    loadingData.value = true;
    const response = await fetch(
      `http://localhost:8000/api/dispatcher/admin/tables?database_name=${selectedDatabase.value}`,
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    availableTables.value = data.tables;

    // Clear selected table and fields
    selectedTable.value = "";
    tableFields.value = [];
  } catch (error) {
    addNotification({
      type: "error",
      message: "Помилка завантаження таблиць",
    });
  } finally {
    loadingData.value = false;
  }
};

const loadTableFields = async () => {
  if (!selectedDatabase.value || !selectedTable.value) return;

  try {
    loadingData.value = true;
    const response = await fetch(
      `http://localhost:8000/api/dispatcher/admin/table-fields?database_name=${selectedDatabase.value}&table_name=${selectedTable.value}`,
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    tableFields.value = data.fields;
  } catch (error) {
    addNotification({
      type: "error",
      message: "Помилка завантаження полів таблиці",
    });
  } finally {
    loadingData.value = false;
  }
};

// Initialize
onMounted(() => {
  loadDatabases();
});
</script>

<style scoped>
.database-monitor {
  padding: 20px;
  background: #f8f9fa;
  min-height: 100vh;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.monitor-header {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  text-align: center;
}

.monitor-header h1 {
  color: #2c3e50;
  margin: 0 0 10px 0;
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.monitor-subtitle {
  color: #7f8c8d;
  margin: 0;
  font-size: 1.1rem;
}

.monitor-controls {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  display: flex;
  gap: 20px;
  align-items: end;
  flex-wrap: wrap;
}

.database-selector,
.table-selector {
  flex: 1;
  min-width: 200px;
}

.database-selector label,
.table-selector label {
  display: block;
  margin-bottom: 8px;
  color: #2c3e50;
  font-weight: 600;
}

.database-select,
.table-select {
  width: 100%;
  padding: 10px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.database-select:focus,
.table-select:focus {
  outline: none;
  border-color: #3498db;
}

.loading-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #3498db;
  font-weight: 600;
}

.monitor-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.database-overview {
  padding: 30px;
}

.database-overview h3 {
  color: #2c3e50;
  margin: 0 0 25px 0;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.tables-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.table-card {
  border: 2px solid #e1e8ed;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
}

.table-card:hover {
  border-color: #3498db;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(52, 152, 219, 0.15);
}

.table-header {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.table-header h4 {
  color: #2c3e50;
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  text-align: center;
  padding: 8px 0;
  border-bottom: 2px solid #f0f0f0;
}

.table-stats {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-top: 8px;
}

.table-records {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(52, 152, 219, 0.3);
}

.table-columns {
  background: linear-gradient(135deg, #27ae60, #229954);
  color: white;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(39, 174, 96, 0.3);
}

.table-records i,
.table-columns i {
  font-size: 0.9rem;
}

.table-actions {
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  background: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background: #2980b9;
}

.table-structure {
  padding: 30px;
}

.structure-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

.structure-header h3 {
  color: #2c3e50;
  margin: 0;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.structure-info {
  display: flex;
  gap: 10px;
}

.info-badge {
  background: #e74c3c;
  color: white;
  padding: 5px 12px;
  border-radius: 15px;
  font-size: 0.9rem;
  font-weight: 600;
}

.fields-search {
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  max-width: 300px;
  padding: 10px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #3498db;
}

.fields-table {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.table th {
  background: #f8f9fa;
  padding: 12px;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e1e8ed;
}

.table td {
  padding: 12px;
  border-bottom: 1px solid #e1e8ed;
  vertical-align: top;
}

.key-field {
  background: #fff9e6;
}

.field-name {
  font-weight: 600;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 8px;
}

.key-icon {
  color: #f39c12;
}

.field-type {
  font-family: "Courier New", monospace;
  background: #f8f9fa;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.nullable-yes {
  color: #27ae60;
  font-weight: 600;
}

.nullable-no {
  color: #e74c3c;
  font-weight: 600;
}

.field-key {
  text-align: center;
  color: #f39c12;
}

.field-default {
  font-family: "Courier New", monospace;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.samples {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.sample-value {
  background: #e8f4f8;
  color: #2c3e50;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-family: "Courier New", monospace;
}

.no-samples {
  color: #bdc3c7;
}

.empty-state {
  padding: 60px 30px;
  text-align: center;
  color: #7f8c8d;
}

.empty-state i {
  font-size: 4rem;
  margin-bottom: 20px;
  color: #bdc3c7;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin: 0 0 10px 0;
}

.empty-state p {
  font-size: 1.1rem;
  margin: 0;
}

/* Responsive design */
@media (max-width: 768px) {
  .monitor-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .structure-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .tables-grid {
    grid-template-columns: 1fr;
  }

  .table {
    font-size: 0.9rem;
  }

  .table th,
  .table td {
    padding: 8px;
  }
}
</style>
