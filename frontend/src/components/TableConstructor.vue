<template>
  <div class="table-constructor">
    <div class="constructor-header">
      <h2>
        <i class="fas fa-table" />
        Конструктор таблиць
      </h2>
      <p class="constructor-subtitle">
        Створюйте кастомні таблиці з потрібними стовпцями
      </p>
    </div>

    <div class="constructor-content">
      <!-- Left Panel - Configuration -->
      <div class="config-panel">
        <div class="config-section">
          <h3>
            <i class="fas fa-cog" />
            Налаштування таблиці
          </h3>

          <!-- Table Name -->
          <div class="form-group">
            <label>Назва таблиці:</label>
            <input
              v-model="currentTable.name"
              type="text"
              placeholder="Введіть назву таблиці"
              class="form-input"
            />
          </div>

          <!-- Description -->
          <div class="form-group">
            <label>Опис:</label>
            <textarea
              v-model="currentTable.description"
              placeholder="Опис таблиці (необов'язково)"
              class="form-textarea"
              rows="3"
            />
          </div>

          <!-- Data Source -->
          <div class="form-group">
            <label>Джерело даних:</label>
            <select
              v-model="currentTable.database"
              class="form-select"
              @change="loadDatabaseTables"
            >
              <option value="">Виберіть базу даних</option>
              <option v-for="db in availableDatabases" :key="db" :value="db">
                {{ db }}
              </option>
            </select>
          </div>

          <div v-if="currentTable.database" class="form-group">
            <label>Таблиця:</label>
            <select
              v-model="currentTable.sourceTable"
              class="form-select"
              @change="loadTableColumns"
            >
              <option value="">Виберіть таблицю</option>
              <option
                v-for="table in availableTables"
                :key="table.name"
                :value="table.name"
              >
                {{ table.name }} ({{ table.row_count }} записів)
              </option>
            </select>
          </div>
        </div>

        <!-- Column Selection -->
        <div v-if="currentTable.sourceTable" class="config-section">
          <h3>
            <i class="fas fa-columns" />
            Вибір стовпців
          </h3>

          <div class="column-actions-bar">
            <div class="column-search">
              <input
                v-model="columnSearch"
                type="text"
                placeholder="Пошук стовпців..."
                class="search-input"
              />
            </div>
            <button
              class="btn-custom-field"
              @click="showCustomFieldBuilder = true"
            >
              <i class="fas fa-plus-circle" />
              Кастомне поле
            </button>
          </div>

          <div class="columns-list">
            <div
              v-for="column in filteredColumns"
              :key="column.name"
              class="column-item"
              :class="{ selected: isColumnSelected(column.name) }"
              @click="toggleColumn(column)"
            >
              <div class="column-info">
                <div class="column-name">
                  <i v-if="column.is_key" class="fas fa-key key-icon" />
                  <i v-if="column.is_custom" class="fas fa-magic custom-icon" />
                  {{ column.name }}
                </div>
                <div class="column-type">{{ column.type }}</div>
              </div>
              <div class="column-actions">
                <i
                  v-if="isColumnSelected(column.name)"
                  class="fas fa-check selected-icon"
                />
                <i v-else class="fas fa-plus add-icon" />
              </div>
            </div>
          </div>

          <!-- Custom Fields Section -->
          <div v-if="customFields.length > 0" class="custom-fields-section">
            <h4>
              <i class="fas fa-magic" />
              Кастомні поля
            </h4>
            <div class="custom-fields-list">
              <div
                v-for="field in customFields"
                :key="field.id"
                class="custom-field-item"
                :class="{ selected: isCustomFieldSelected(field.name) }"
                @click="toggleCustomField(field)"
              >
                <div class="field-info">
                  <div class="field-name">
                    <i class="fas fa-magic custom-icon" />
                    {{ field.label }}
                  </div>
                  <div class="field-type">{{ getFieldTypeName(field.type) }}</div>
                  <div v-if="field.description" class="field-description">
                    {{ field.description }}
                  </div>
                </div>
                <div class="field-actions">
                  <button
                    class="btn-edit-field"
                    @click.stop="editCustomField(field)"
                  >
                    <i class="fas fa-edit" />
                  </button>
                  <button
                    class="btn-delete-field"
                    @click.stop="deleteCustomField(field.id)"
                  >
                    <i class="fas fa-trash" />
                  </button>
                  <i
                    v-if="isCustomFieldSelected(field.name)"
                    class="fas fa-check selected-icon"
                  />
                  <i v-else class="fas fa-plus add-icon" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="config-actions">
          <button
            :disabled="!canSaveTable"
            class="btn-primary"
            @click="saveTable"
          >
            <i class="fas fa-save" />
            Зберегти таблицю
          </button>
          <button class="btn-secondary" @click="resetTable">
            <i class="fas fa-undo" />
            Скинути
          </button>
          <button class="btn-danger" @click="clearAllData">
            <i class="fas fa-trash" />
            Очистити всі дані
          </button>
        </div>
      </div>

      <!-- Right Panel - Preview -->
      <div class="preview-panel">
        <div class="preview-header">
          <h3>
            <i class="fas fa-eye" />
            Превью таблиці
          </h3>
          <div v-if="currentTable.name" class="preview-info">
            <span class="table-name">{{ currentTable.name }}</span>
            <span class="column-count"
              >{{ currentTable.columns.length }} стовпців</span
            >
          </div>
        </div>

        <div v-if="currentTable.columns.length > 0" class="preview-content">
          <!-- Column Configuration -->
          <div class="selected-columns">
            <h4>Обрані стовпці:</h4>
            <div class="columns-config">
              <div
                v-for="(column, index) in currentTable.columns"
                :key="column.field"
                class="column-config"
              >
                <div class="column-order">
                  <button
                    :disabled="index === 0"
                    class="order-btn"
                    @click="moveColumn(index, -1)"
                  >
                    <i class="fas fa-chevron-up" />
                  </button>
                  <span class="order-number">{{ index + 1 }}</span>
                  <button
                    :disabled="index === currentTable.columns.length - 1"
                    class="order-btn"
                    @click="moveColumn(index, 1)"
                  >
                    <i class="fas fa-chevron-down" />
                  </button>
                </div>

                <div class="column-details">
                  <input
                    v-model="column.label"
                    type="text"
                    placeholder="Назва стовпця"
                    class="column-label-input"
                  />
                  <div class="column-field">{{ column.field }}</div>
                  <div class="column-type-info">{{ column.type }}</div>
                </div>

                <div class="column-actions">
                  <button class="remove-btn" @click="removeColumn(index)">
                    <i class="fas fa-times" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Table Preview -->
          <div v-if="previewData.length > 0" class="table-preview">
            <h4>Превью даних:</h4>
            <div class="preview-table-container">
              <table class="preview-table">
                <thead>
                  <tr>
                    <th
                      v-for="column in currentTable.columns"
                      :key="column.field"
                    >
                      {{ column.label || column.field }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, index) in previewData" :key="index">
                    <td
                      v-for="column in currentTable.columns"
                      :key="column.field"
                    >
                      {{ row[column.field] || "-" }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div v-else class="empty-preview">
          <i class="fas fa-table" />
          <h4>Виберіть стовпці для превью</h4>
          <p>Оберіть стовпці зліва для створення таблиці</p>
        </div>
      </div>
    </div>

    <!-- Saved Tables Section -->
    <div v-if="savedTables.length > 0" class="saved-tables">
      <h3>
        <i class="fas fa-list" />
        Збережені таблиці
      </h3>
      <div class="tables-grid">
        <div v-for="table in savedTables" :key="table.id || 'table'" class="table-card">
          <div class="table-card-header">
            <h4>{{ table.name }}</h4>
            <div class="table-meta">
              <span class="column-count"
                >{{ table.columns.length }} стовпців</span
              >
              <span class="source-info"
                >{{ table.database }}.{{ table.sourceTable }}</span
              >
            </div>
          </div>
          <div v-if="table.description" class="table-description">
            {{ table.description }}
          </div>
          <div class="table-actions">
            <button class="btn-edit" @click="editTable(table)">
              <i class="fas fa-edit" />
              Редагувати
            </button>
            <button class="btn-view" @click="viewTable(table)">
              <i class="fas fa-eye" />
              Переглянути
            </button>
            <button class="btn-delete" @click="deleteTable(table.id || '')">
              <i class="fas fa-trash" />
              Видалити
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Table Viewer Modal -->
    <div v-if="showTableViewer" class="modal-overlay" @click="closeTableViewer">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>
            <i class="fas fa-table" />
            {{ viewingTable?.name || "Таблиця" }}
          </h3>
          <button class="close-btn" @click="closeTableViewer">
            <i class="fas fa-times" />
          </button>
        </div>

        <div class="modal-body">
          <div v-if="viewingTable" class="table-info">
            <div class="table-info-content">
              <div class="info-details">
                <div class="info-row">
                  <span class="info-label">Джерело:</span>
                  <span class="info-value"
                    >{{ viewingTable.database }}.{{
                      viewingTable.sourceTable
                    }}</span
                  >
                </div>
                <div class="info-row">
                  <span class="info-label">Стовпців:</span>
                  <span class="info-value">{{ viewingTable.columns.length }}</span>
                </div>
                <div v-if="viewingTable.description" class="info-row">
                  <span class="info-label">Опис:</span>
                  <span class="info-value">{{ viewingTable.description }}</span>
                </div>
              </div>
              <div class="info-actions">
                <button class="print-btn" @click="showPrintModal = true">
                  <i class="fas fa-print" />
                  Друкувати форму
                </button>
              </div>
            </div>
          </div>

          <div v-if="viewingLoading" class="loading-state">
            <i class="fas fa-spinner fa-spin" />
            <p>Завантаження даних...</p>
          </div>

          <div v-else-if="viewingTableData.length > 0" class="table-data">
            <div class="data-table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th
                      v-for="column in viewingTable?.columns"
                      :key="column.field"
                    >
                      {{ column.label || column.field }}
                      <span class="column-type">{{ column.type }}</span>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, index) in viewingTableData" :key="index">
                    <td
                      v-for="column in viewingTable?.columns"
                      :key="column.field"
                    >
                      {{ row[column.field] || "-" }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-else class="no-data">
            <i class="fas fa-inbox" />
            <p>Немає даних для відображення</p>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-secondary" @click="closeTableViewer">
            <i class="fas fa-times" />
            Закрити
          </button>
        </div>
      </div>
    </div>

    <!-- Custom Field Builder Modal -->
    <div v-if="showCustomFieldBuilder" class="modal-overlay" @click="closeCustomFieldBuilder">
      <div class="modal-content custom-field-modal" @click.stop>
        <CustomFieldBuilder
          :available-fields="sourceColumns"
          :available-tables="availableTables"
          :database="currentTable.database"
          :source-table="currentTable.sourceTable"
          :editing-field="editingCustomField"
          @close="closeCustomFieldBuilder"
          @save="saveCustomField"
        />
      </div>
    </div>

    <!-- Print Modal -->
    <div v-if="showPrintModal" class="modal-overlay" @click="showPrintModal = false">
      <div class="modal-content print-modal" @click.stop>
        <div class="modal-header">
          <h3>
            <i class="fas fa-print" />
            Друкувати форму
          </h3>
          <button class="close-btn" @click="showPrintModal = false">
            <i class="fas fa-times" />
          </button>
        </div>
        <div class="modal-body">
          <div class="greeting-content">
            <h2>Вітаємо!</h2>
            <p>Це модальне вікно для друкування форми. Функціонал друкування буде реалізований пізніше.</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showPrintModal = false">
            Закрити
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, defineAsyncComponent } from "vue";
import { useNotifications } from "@/composables/useNotifications";

const CustomFieldBuilder = defineAsyncComponent(() => import('./CustomFieldBuilder.vue'));

const { addNotification } = useNotifications();

// Types
interface Column {
  field: string;
  label: string;
  type: string;
  is_key?: boolean;
}

interface CustomTable {
  id?: string;
  name: string;
  description: string;
  database: string;
  sourceTable: string;
  columns: Column[];
  createdAt?: string;
  updatedAt?: string;
}

interface DatabaseColumn {
  name: string;
  type: string;
  nullable: boolean;
  is_key: boolean;
  default_value: string;
  sample_values: string[];
  is_custom?: boolean;
}

interface CustomField {
  id: string;
  name: string;
  label: string;
  type: string;
  description?: string;
  config: Record<string, unknown>;
  sql?: string;
}

// Reactive state
const currentTable = ref<CustomTable>({
  name: "",
  description: "",
  database: "",
  sourceTable: "",
  columns: [],
});

const availableDatabases = ref<string[]>([]);
const availableTables = ref<Array<{ name: string; row_count: number }>>([]);
const sourceColumns = ref<DatabaseColumn[]>([]);
const savedTables = ref<CustomTable[]>([]);
const previewData = ref<Record<string, unknown>[]>([]);
const columnSearch = ref<string>("");
const loading = ref<boolean>(false);

// Custom fields state
const customFields = ref<CustomField[]>([]);
const showCustomFieldBuilder = ref<boolean>(false);
const editingCustomField = ref<CustomField | null>(null);

// Table viewer state
const showTableViewer = ref<boolean>(false);
const viewingTable = ref<CustomTable | null>(null);
const viewingTableData = ref<Record<string, unknown>[]>([]);
const viewingLoading = ref<boolean>(false);

// Print modal state
const showPrintModal = ref<boolean>(false);

// Computed properties
const filteredColumns = computed(() => {
  if (!columnSearch.value) return sourceColumns.value;
  return sourceColumns.value.filter(
    (col) =>
      col.name.toLowerCase().includes(columnSearch.value.toLowerCase()) ||
      col.type.toLowerCase().includes(columnSearch.value.toLowerCase()),
  );
});

const canSaveTable = computed(() => {
  return (
    currentTable.value.name.trim() !== "" &&
    currentTable.value.database !== "" &&
    currentTable.value.sourceTable !== "" &&
    currentTable.value.columns.length > 0
  );
});

// Methods
const isColumnSelected = (columnName: string): boolean => {
  return currentTable.value.columns.some((col) => col.field === columnName);
};

const toggleColumn = (column: DatabaseColumn): void => {
  const index = currentTable.value.columns.findIndex(
    (col) => col.field === column.name,
  );

  if (index > -1) {
    currentTable.value.columns.splice(index, 1);
  } else {
    currentTable.value.columns.push({
      field: column.name,
      label: column.name,
      type: column.type,
      is_key: column.is_key,
    });
  }

  loadPreviewData();
};

const removeColumn = (index: number): void => {
  currentTable.value.columns.splice(index, 1);
  loadPreviewData();
};

const moveColumn = (index: number, direction: number): void => {
  const newIndex = index + direction;
  if (newIndex >= 0 && newIndex < currentTable.value.columns.length) {
    const columns = currentTable.value.columns;
    const temp = columns[index];
    const newTemp = columns[newIndex];
    if (temp && newTemp) {
      [columns[index], columns[newIndex]] = [newTemp, temp];
    }
  }
};

const resetTable = (): void => {
  currentTable.value = {
    name: "",
    description: "",
    database: "",
    sourceTable: "",
    columns: [],
  };
  sourceColumns.value = [];
  previewData.value = [];
  columnSearch.value = "";
};

const clearAllData = (): void => {
  if (confirm('Ви впевнені, що хочете очистити всі збережені таблиці та кастомні поля?')) {
    localStorage.removeItem('khtrm-custom-tables');
    localStorage.removeItem('khtrm-custom-fields');
    savedTables.value = [];
    customFields.value = [];
    resetTable();
    
    addNotification({
      type: 'success',
      message: 'Всі дані очищено'
    });
  }
};

// API Methods
const loadDatabases = async (): Promise<void> => {
  try {
    loading.value = true;
    const response = await fetch(
      "http://localhost:8000/api/dispatcher/admin/databases",
    );
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    availableDatabases.value = data.databases;
  } catch (error) {
    addNotification({
      type: "error",
      message: "Помилка завантаження баз даних",
    });
  } finally {
    loading.value = false;
  }
};

const loadDatabaseTables = async (): Promise<void> => {
  if (!currentTable.value.database) return;

  try {
    loading.value = true;
    const response = await fetch(
      `http://localhost:8000/api/dispatcher/admin/tables?database_name=${currentTable.value.database}`,
    );
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    availableTables.value = data.tables;

    // Reset dependent fields
    currentTable.value.sourceTable = "";
    sourceColumns.value = [];
    currentTable.value.columns = [];
  } catch (error) {
    addNotification({
      type: "error",
      message: "Помилка завантаження таблиць",
    });
  } finally {
    loading.value = false;
  }
};

const loadTableColumns = async (): Promise<void> => {
  if (!currentTable.value.database || !currentTable.value.sourceTable) return;

  try {
    loading.value = true;
    const response = await fetch(
      `http://localhost:8000/api/dispatcher/admin/table-fields?database_name=${currentTable.value.database}&table_name=${currentTable.value.sourceTable}`,
    );
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    sourceColumns.value = data.fields;

    // Reset columns
    currentTable.value.columns = [];
  } catch (error) {
    addNotification({
      type: "error",
      message: "Помилка завантаження стовпців",
    });
  } finally {
    loading.value = false;
  }
};

const loadPreviewData = async (): Promise<void> => {
  if (
    !currentTable.value.database ||
    !currentTable.value.sourceTable ||
    currentTable.value.columns.length === 0
  ) {
    previewData.value = [];
    return;
  }

  try {
    // Check if table has custom fields
    const hasCustomFields = currentTable.value.columns.some((col) => 
      customFields.value.some((cf) => cf.name === col.field)
    );
    
    console.log('Preview - Table columns:', currentTable.value.columns);
    console.log('Preview - Custom fields:', customFields.value);
    console.log('Preview - Has custom fields:', hasCustomFields);

    if (hasCustomFields) {
      // Use the new custom table data endpoint
      const customFieldsData = currentTable.value.columns
        .filter((col) => customFields.value.some((cf) => cf.name === col.field))
        .map((col) => {
          const customField = customFields.value.find((cf) => cf.name === col.field);
          return customField;
        })
        .filter(Boolean);

      const regularColumns = currentTable.value.columns.filter((col) => 
        !customFields.value.some((cf) => cf.name === col.field)
      );

      const requestBody = {
        columns: regularColumns,
        custom_fields: customFieldsData,
      };

      const response = await fetch(
        `http://localhost:8000/api/dispatcher/admin/custom-table-data?database_name=${currentTable.value.database}&table_name=${currentTable.value.sourceTable}&limit=3`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      previewData.value = data.data || [];
    } else {
      // Use the regular table data endpoint
      const columnNames = currentTable.value.columns.map((col) => col.field).join(", ");
      
      const response = await fetch(
        `http://localhost:8000/api/dispatcher/admin/table-data?database_name=${currentTable.value.database}&table_name=${currentTable.value.sourceTable}&columns=${columnNames}&limit=3`,
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      previewData.value = data.data || [];
    }
  } catch (error) {
    console.error("Error loading preview data:", error);
    
    // Fallback to mock data
    previewData.value = [
      { id: 1, name: "Приклад 1", value: "Значення 1" },
      { id: 2, name: "Приклад 2", value: "Значення 2" },
      { id: 3, name: "Приклад 3", value: "Значення 3" },
    ];
  }
};

const saveTable = async (): Promise<void> => {
  if (!canSaveTable.value) return;

  try {
    loading.value = true;

    // For now, save to localStorage
    const tableToSave = {
      ...currentTable.value,
      id: currentTable.value.id || Date.now().toString(),
      createdAt: currentTable.value.createdAt || new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    const existingIndex = savedTables.value.findIndex(
      (t) => t.id === tableToSave.id,
    );
    if (existingIndex > -1) {
      savedTables.value[existingIndex] = tableToSave;
    } else {
      savedTables.value.push(tableToSave);
    }

    // Save to localStorage
    localStorage.setItem(
      "khtrm-custom-tables",
      JSON.stringify(savedTables.value),
    );

    addNotification({
      type: "success",
      message: "Таблицю успішно збережено!",
    });

    resetTable();
  } catch (error) {
    addNotification({
      type: "error",
      message: "Помилка збереження таблиці",
    });
  } finally {
    loading.value = false;
  }
};

const editTable = async (table: CustomTable): Promise<void> => {
  currentTable.value = { ...table };

  // Scroll to top to show the edit form
  window.scrollTo({ top: 0, behavior: "smooth" });

  // Load databases first
  await loadDatabaseTables();

  // Restore the source table after loading
  currentTable.value.sourceTable = table.sourceTable;

  // Load table columns
  await loadTableColumns();

  // Restore the columns after loading
  currentTable.value.columns = [...table.columns];

  addNotification({
    type: "info",
    message: `Редагування таблиці "${table.name}"`,
  });
};

const viewTable = async (table: CustomTable): Promise<void> => {
  viewingTable.value = table;
  showTableViewer.value = true;

  // Load actual data from the database
  await loadTableData(table);
};

const loadTableData = async (table: CustomTable): Promise<void> => {
  if (!table.database || !table.sourceTable || table.columns.length === 0) {
    return;
  }

  try {
    viewingLoading.value = true;

    // Check if table has custom fields
    const hasCustomFields = table.columns.some((col) => 
      customFields.value.some((cf) => cf.name === col.field)
    );
    
    console.log('Table columns:', table.columns);
    console.log('Custom fields:', customFields.value);
    console.log('Has custom fields:', hasCustomFields);

    if (hasCustomFields) {
      // Use the new custom table data endpoint
      const customFieldsData = table.columns
        .filter((col) => customFields.value.some((cf) => cf.name === col.field))
        .map((col) => {
          const customField = customFields.value.find((cf) => cf.name === col.field);
          return customField;
        })
        .filter(Boolean);

      const regularColumns = table.columns.filter((col) => 
        !customFields.value.some((cf) => cf.name === col.field)
      );

      const requestBody = {
        columns: regularColumns,
        custom_fields: customFieldsData,
      };

      console.log('Request body:', requestBody);
      
      const response = await fetch(
        `http://localhost:8000/api/dispatcher/admin/custom-table-data?database_name=${table.database}&table_name=${table.sourceTable}&limit=10`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Custom table data error:', errorText);
        throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log('Custom table data response:', data);
      viewingTableData.value = data.data || [];
    } else {
      // Use the regular table data endpoint
      const columnNames = table.columns.map((col) => col.field).join(", ");
      
      const response = await fetch(
        `http://localhost:8000/api/dispatcher/admin/table-data?database_name=${table.database}&table_name=${table.sourceTable}&columns=${columnNames}&limit=10`,
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      viewingTableData.value = data.data || [];
    }
  } catch (error) {
    console.error("Error loading table data:", error);

    // Fallback to mock data
    viewingTableData.value = Array.from({ length: 10 }, (_, i) => {
      const row: Record<string, unknown> = {};
      table.columns.forEach((col) => {
        row[col.field] = `Значення ${i + 1}`;
      });
      return row;
    });

    addNotification({
      type: "warning",
      message: "Завантажено тестові дані. API endpoint не доступний.",
    });
  } finally {
    viewingLoading.value = false;
  }
};

const closeTableViewer = (): void => {
  showTableViewer.value = false;
  viewingTable.value = null;
  viewingTableData.value = [];
};

const deleteTable = (tableId: string): void => {
  if (confirm("Ви впевнені, що хочете видалити цю таблицю?")) {
    savedTables.value = savedTables.value.filter((t) => t.id !== tableId);
    localStorage.setItem(
      "khtrm-custom-tables",
      JSON.stringify(savedTables.value),
    );

    addNotification({
      type: "success",
      message: "Таблицю видалено",
    });
  }
};

const loadSavedTables = (): void => {
  const saved = localStorage.getItem("khtrm-custom-tables");
  if (saved) {
    try {
      savedTables.value = JSON.parse(saved);
    } catch (error) {
      console.error("Error loading saved tables:", error);
    }
  }
};

const loadCustomFields = (): void => {
  const saved = localStorage.getItem("khtrm-custom-fields");
  if (saved) {
    try {
      customFields.value = JSON.parse(saved);
    } catch (error) {
      console.error("Error loading custom fields:", error);
    }
  }
};

const saveCustomFieldsToStorage = (): void => {
  localStorage.setItem("khtrm-custom-fields", JSON.stringify(customFields.value));
};

// Custom field methods
const isCustomFieldSelected = (fieldId: string): boolean => {
  return currentTable.value.columns.some((col) => col.field === fieldId);
};

const toggleCustomField = (field: CustomField): void => {
  const index = currentTable.value.columns.findIndex(
    (col) => col.field === field.name
  );

  if (index > -1) {
    currentTable.value.columns.splice(index, 1);
  } else {
    currentTable.value.columns.push({
      field: field.name,
      label: field.label,
      type: field.type,
      is_key: false,
    });
  }

  loadPreviewData();
};

const getFieldTypeName = (type: string): string => {
  const typeNames: Record<string, string> = {
    calculated: 'Обчислюване',
    join: 'Об\'єднання',
    aggregate: 'Агрегатне',
    lookup: 'Пошук'
  };
  return typeNames[type] || type;
};

const saveCustomField = (field: CustomField): void => {
  if (editingCustomField.value) {
    // Update existing field
    const index = customFields.value.findIndex(f => f.id === editingCustomField.value!.id);
    if (index > -1) {
      const oldField = customFields.value[index];
      if (oldField) {
        customFields.value[index] = { ...field, id: oldField.id };
        
        // Update column references if field name changed
        if (oldField.name !== field.name) {
          currentTable.value.columns = currentTable.value.columns.map(col => 
            col.field === oldField.name ? { ...col, field: field.name, label: field.label } : col
          );
        }
      }
    }
    editingCustomField.value = null;
  } else {
    // Add new field
    customFields.value.push(field);
  }
  
  saveCustomFieldsToStorage();
  closeCustomFieldBuilder();
  loadPreviewData();
};

const editCustomField = (field: CustomField): void => {
  editingCustomField.value = field;
  showCustomFieldBuilder.value = true;
};

const deleteCustomField = (fieldId: string): void => {
  if (confirm('Ви впевнені, що хочете видалити це кастомне поле?')) {
    const fieldToDelete = customFields.value.find(f => f.id === fieldId);
    customFields.value = customFields.value.filter(f => f.id !== fieldId);
    
    // Remove from selected columns if it's there
    if (fieldToDelete) {
      currentTable.value.columns = currentTable.value.columns.filter(
        col => col.field !== fieldToDelete.name
      );
    }
    
    saveCustomFieldsToStorage();
    loadPreviewData();
    
    addNotification({
      type: 'success',
      message: 'Кастомне поле видалено'
    });
  }
};

const closeCustomFieldBuilder = (): void => {
  showCustomFieldBuilder.value = false;
  editingCustomField.value = null;
};

// Initialize
onMounted(() => {
  loadDatabases();
  loadSavedTables();
  loadCustomFields();
});

// Define component options for proper TypeScript support
defineOptions({
  name: 'TableConstructor'
});
</script>

<style scoped>
.table-constructor {
  padding: 20px;
  background: #f8f9fa;
  min-height: 100vh;
}

.constructor-header {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  text-align: center;
}

.constructor-header h2 {
  color: #2c3e50;
  margin: 0 0 10px 0;
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.constructor-subtitle {
  color: #7f8c8d;
  margin: 0;
  font-size: 1.1rem;
}

.constructor-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.config-panel,
.preview-panel {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.config-section {
  padding: 25px;
  border-bottom: 1px solid #e1e8ed;
}

.config-section:last-child {
  border-bottom: none;
}

.config-section h3 {
  color: #2c3e50;
  margin: 0 0 20px 0;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #2c3e50;
  font-weight: 600;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3498db;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.column-search {
  margin-bottom: 15px;
}

.search-input {
  width: 100%;
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

.columns-list {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e1e8ed;
  border-radius: 8px;
}

.column-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #e1e8ed;
  cursor: pointer;
  transition: background-color 0.3s;
}

.column-item:hover {
  background: #f8f9fa;
}

.column-item.selected {
  background: #e8f4f8;
  border-left: 4px solid #3498db;
}

.column-item:last-child {
  border-bottom: none;
}

.column-info {
  flex: 1;
}

.column-name {
  font-weight: 600;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 8px;
}

.key-icon {
  color: #f39c12;
  font-size: 0.9rem;
}

.column-type {
  font-size: 0.9rem;
  color: #7f8c8d;
  font-family: "Courier New", monospace;
}

.column-actions {
  display: flex;
  align-items: center;
}

.selected-icon {
  color: #27ae60;
}

.add-icon {
  color: #3498db;
}

.custom-icon {
  color: #9b59b6;
}

.column-actions-bar {
  display: flex;
  gap: 15px;
  align-items: center;
  margin-bottom: 15px;
}

.column-actions-bar .column-search {
  flex: 1;
  margin-bottom: 0;
}

.btn-custom-field {
  background: #9b59b6;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
  font-size: 0.9rem;
}

.btn-custom-field:hover {
  background: #8e44ad;
}

.custom-fields-section {
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #e1e8ed;
}

.custom-fields-section h4 {
  color: #2c3e50;
  margin: 0 0 15px 0;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.custom-fields-list {
  border: 1px solid #e1e8ed;
  border-radius: 8px;
  max-height: 300px;
  overflow-y: auto;
}

.custom-field-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #e1e8ed;
  transition: background-color 0.3s;
}

.custom-field-item:hover {
  background: #f8f9fa;
}

.custom-field-item.selected {
  background: #f3e5f5;
  border-left: 4px solid #9b59b6;
}

.custom-field-item:last-child {
  border-bottom: none;
}

.field-info {
  flex: 1;
  cursor: pointer;
}

.field-name {
  font-weight: 600;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 5px;
}

.field-type {
  font-size: 0.9rem;
  color: #7f8c8d;
  font-family: "Courier New", monospace;
  margin-bottom: 5px;
}

.field-description {
  font-size: 0.85rem;
  color: #95a5a6;
  line-height: 1.3;
}

.field-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-edit-field,
.btn-delete-field {
  background: none;
  border: none;
  padding: 6px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.btn-edit-field {
  color: #3498db;
}

.btn-edit-field:hover {
  background: #3498db;
  color: white;
}

.btn-delete-field {
  color: #e74c3c;
}

.btn-delete-field:hover {
  background: #e74c3c;
  color: white;
}

.custom-field-modal {
  max-width: 900px;
  width: 90vw;
}

.custom-field-modal .modal-content {
  padding: 0;
}

.config-actions {
  padding: 25px;
  display: flex;
  gap: 15px;
}

.btn-primary,
.btn-secondary,
.btn-danger {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
}

.btn-primary:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background: #c0392b;
}

.preview-panel {
  display: flex;
  flex-direction: column;
}

.preview-header {
  padding: 25px;
  border-bottom: 1px solid #e1e8ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-header h3 {
  color: #2c3e50;
  margin: 0;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.preview-info {
  display: flex;
  flex-direction: column;
  align-items: end;
}

.table-name {
  font-weight: 600;
  color: #2c3e50;
}

.column-count {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.preview-content {
  padding: 25px;
  flex: 1;
  overflow-y: auto;
}

.selected-columns h4 {
  color: #2c3e50;
  margin: 0 0 15px 0;
}

.columns-config {
  margin-bottom: 30px;
}

.column-config {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px;
  border: 1px solid #e1e8ed;
  border-radius: 8px;
  margin-bottom: 10px;
  background: #f8f9fa;
}

.column-order {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.order-btn {
  background: #3498db;
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
  font-size: 12px;
}

.order-btn:hover:not(:disabled) {
  background: #2980b9;
}

.order-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.order-number {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
}

.column-details {
  flex: 1;
}

.column-label-input {
  width: 100%;
  padding: 6px;
  border: 1px solid #e1e8ed;
  border-radius: 4px;
  font-weight: 600;
  margin-bottom: 5px;
}

.column-field {
  font-size: 0.9rem;
  color: #7f8c8d;
  font-family: "Courier New", monospace;
}

.column-type-info {
  font-size: 0.8rem;
  color: #95a5a6;
}

.remove-btn {
  background: #e74c3c;
  color: white;
  border: none;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
  font-size: 14px;
}

.remove-btn:hover {
  background: #c0392b;
}

.table-preview h4 {
  color: #2c3e50;
  margin: 0 0 15px 0;
}

.preview-table-container {
  max-height: 300px;
  overflow: auto;
  border: 1px solid #e1e8ed;
  border-radius: 8px;
}

.preview-table {
  width: 100%;
  border-collapse: collapse;
}

.preview-table th {
  background: #f8f9fa;
  padding: 12px;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e1e8ed;
  position: sticky;
  top: 0;
}

.preview-table td {
  padding: 12px;
  border-bottom: 1px solid #e1e8ed;
  color: #2c3e50;
}

.empty-preview {
  padding: 60px 25px;
  text-align: center;
  color: #7f8c8d;
}

.empty-preview i {
  font-size: 4rem;
  margin-bottom: 20px;
  color: #bdc3c7;
}

.empty-preview h4 {
  margin: 0 0 10px 0;
  color: #7f8c8d;
}

.empty-preview p {
  margin: 0;
}

.saved-tables {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.saved-tables h3 {
  color: #2c3e50;
  margin: 0 0 25px 0;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.tables-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.table-card {
  border: 2px solid #e1e8ed;
  border-radius: 10px;
  padding: 20px;
  transition: all 0.3s;
}

.table-card:hover {
  border-color: #3498db;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.table-card-header h4 {
  color: #2c3e50;
  margin: 0 0 10px 0;
  font-size: 1.2rem;
}

.table-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

.column-count {
  background: #3498db;
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.source-info {
  color: #7f8c8d;
  font-size: 0.9rem;
  font-family: "Courier New", monospace;
}

.table-description {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-bottom: 15px;
  line-height: 1.4;
}

.table-actions {
  display: flex;
  gap: 10px;
}

.btn-edit,
.btn-view,
.btn-delete {
  flex: 1;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.btn-edit {
  background: #3498db;
  color: white;
}

.btn-edit:hover {
  background: #2980b9;
}

.btn-view {
  background: #27ae60;
  color: white;
}

.btn-view:hover {
  background: #219a52;
}

.btn-delete {
  background: #e74c3c;
  color: white;
}

.btn-delete:hover {
  background: #c0392b;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 90vw;
  max-height: 90vh;
  width: 1200px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 20px 25px;
  border-bottom: 1px solid #e1e8ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f9fa;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.3rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #7f8c8d;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  transition: all 0.3s;
}

.close-btn:hover {
  background: #e74c3c;
  color: white;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 25px;
}

.table-info {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.table-info-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.info-details {
  flex: 1;
}

.info-actions {
  display: flex;
  align-items: flex-start;
}

.info-row {
  display: flex;
  margin-bottom: 8px;
}

.info-row:last-child {
  margin-bottom: 0;
}

.info-label {
  font-weight: 600;
  color: #2c3e50;
  min-width: 80px;
}

.info-value {
  color: #7f8c8d;
  font-family: "Courier New", monospace;
}

.print-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.2s;
}

.print-btn:hover {
  background: #2980b9;
}

.print-btn i {
  font-size: 0.8rem;
}

.print-modal .modal-content {
  max-width: 400px;
}

.greeting-content {
  text-align: center;
  padding: 20px;
}

.greeting-content h2 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.greeting-content p {
  color: #7f8c8d;
  line-height: 1.6;
}

.loading-state {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}

.loading-state i {
  font-size: 2rem;
  margin-bottom: 15px;
  color: #3498db;
}

.loading-state p {
  margin: 0;
  font-size: 1.1rem;
}

.table-data {
  flex: 1;
}

.data-table-container {
  max-height: 500px;
  overflow: auto;
  border: 1px solid #e1e8ed;
  border-radius: 8px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.data-table th {
  background: #f8f9fa;
  padding: 12px;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e1e8ed;
  position: sticky;
  top: 0;
  z-index: 1;
}

.column-type {
  display: block;
  font-size: 0.8rem;
  color: #7f8c8d;
  font-weight: normal;
  font-family: "Courier New", monospace;
}

.data-table td {
  padding: 12px;
  border-bottom: 1px solid #e1e8ed;
  color: #2c3e50;
  vertical-align: top;
}

.data-table tr:hover {
  background: #f8f9fa;
}

.no-data {
  text-align: center;
  padding: 60px;
  color: #7f8c8d;
}

.no-data i {
  font-size: 3rem;
  margin-bottom: 15px;
  color: #bdc3c7;
}

.no-data p {
  margin: 0;
  font-size: 1.1rem;
}

.modal-footer {
  padding: 20px 25px;
  border-top: 1px solid #e1e8ed;
  display: flex;
  justify-content: flex-end;
  background: #f8f9fa;
}

/* Responsive design */
@media (max-width: 1200px) {
  .constructor-content {
    grid-template-columns: 1fr;
  }

  .tables-grid {
    grid-template-columns: 1fr;
  }

  .modal-content {
    width: 95vw;
    max-height: 85vh;
  }
}

@media (max-width: 768px) {
  .table-constructor {
    padding: 15px;
  }

  .constructor-header {
    padding: 20px;
  }

  .constructor-header h2 {
    font-size: 1.5rem;
  }

  .config-section {
    padding: 20px;
  }

  .config-actions {
    flex-direction: column;
  }

  .table-actions {
    flex-direction: column;
  }

  .preview-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .preview-info {
    align-items: flex-start;
  }

  .table-info-content {
    flex-direction: column;
    gap: 15px;
  }

  .info-actions {
    align-self: flex-end;
  }
}
</style>
