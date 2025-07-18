<template>
  <div class="admin-field-settings">
    <div class="settings-header">
      <h2>
        <i class="fas fa-cogs" />
        Налаштування полів для відображення
      </h2>
      <p class="settings-subtitle">
        Керування відображенням полів для різних профілів користувачів
      </p>
    </div>

    <div class="settings-controls">
      <div class="profile-selector">
        <label>Профіль користувача:</label>
        <select v-model="selectedProfile" class="profile-select">
          <option value="dispatcher">Нарядчик</option>
          <option value="timekeeper_a">Табельник A</option>
          <option value="timekeeper_b">Табельник B</option>
          <option value="dispatcher_main">Диспетчер</option>
          <option value="fuel_accountant">Бухгалтер з палива</option>
        </select>
      </div>

      <div class="table-info">
        <span class="info-label">Налаштування для таблиці:</span>
        <span class="info-value">zanaradka (основна таблиця нарядів)</span>
      </div>

      <div class="save-status">
        <span v-if="hasUnsavedChanges" class="unsaved-indicator">
          • Є незбережені зміни
        </span>
        <span v-else class="saved-indicator"> ✓ Всі зміни збережено </span>
      </div>
    </div>

    <div class="settings-content">
      <div class="current-profile-info">
        <h3>
          Налаштування для профілю:
          <span class="profile-name">{{
            getProfileDisplayName(selectedProfile)
          }}</span>
        </h3>
        <p class="table-info">
          База даних: <strong>saltdepoavt_</strong> | Таблиця:
          <strong>zanaradka</strong>
        </p>
        <div class="table-fields-info">
          <p>
            Доступно полів у таблиці:
            <strong>{{ availableFields.length }}</strong>
          </p>
        </div>
      </div>

      <div class="field-management">
        <div class="field-sections">
          <!-- Selected fields with reordering -->
          <div class="selected-fields-section">
            <div class="section-header">
              <h4>
                Обрані поля для відображення ({{ selectedFields.length }}):
              </h4>
              <div class="section-actions">
                <button
                  v-if="selectedFields.length > 0"
                  class="clear-all-btn"
                  title="Очистити всі поля"
                  @click="clearAllFields"
                >
                  Очистити всі
                </button>
                <button
                  class="preset-btn"
                  title="Застосувати стандартні налаштування"
                  @click="applyDefaultPreset"
                >
                  За замовчанням
                </button>
              </div>
            </div>

            <div class="selected-fields-list">
              <div
                v-for="(fieldKey, index) in selectedFields"
                :key="fieldKey"
                class="selected-field-item"
              >
                <div class="field-controls">
                  <button
                    :disabled="index === 0"
                    class="move-btn"
                    title="Перемістити вгору"
                    @click="moveFieldUp(index)"
                  >
                    ↑
                  </button>
                  <button
                    :disabled="index === selectedFields.length - 1"
                    class="move-btn"
                    title="Перемістити вниз"
                    @click="moveFieldDown(index)"
                  >
                    ↓
                  </button>
                </div>
                <span class="field-label">{{ getFieldLabel(fieldKey) }}</span>
                <button
                  class="remove-btn"
                  title="Видалити поле"
                  @click="removeField(fieldKey)"
                >
                  ×
                </button>
              </div>
            </div>
          </div>

          <!-- Available fields to add -->
          <div class="available-fields-section">
            <div class="section-header">
              <h4>Доступні поля для додавання:</h4>
              <div class="search-container">
                <input
                  v-model="fieldSearch"
                  type="text"
                  placeholder="Пошук полів..."
                  class="field-search"
                />
              </div>
            </div>

            <!-- Table and fields are fixed for zanaradka -->

            <div class="available-fields-list">
              <div
                v-for="field in filteredAvailableFields"
                :key="field.key"
                class="available-field-item"
                :title="`Тип: ${field.type}${field.sample_values.length > 0 ? ' | Приклади: ' + field.sample_values.join(', ') : ''}`"
                @click="addField(field.key)"
              >
                <div class="field-info">
                  <span class="field-name">{{ field.label }}</span>
                  <small class="field-type">{{ field.type }}</small>
                  <div
                    v-if="field.sample_values.length > 0"
                    class="field-samples"
                  >
                    <small>{{
                      field.sample_values.slice(0, 2).join(", ")
                    }}</small>
                  </div>
                </div>
                <button class="add-btn" title="Додати поле">+</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="preset-section">
        <h4>Швидкі пресети:</h4>
        <div class="preset-buttons">
          <button
            class="preset-btn dispatcher-preset"
            title="Оптимальна конфігурація для нарядчика"
            @click="applyDispatcherPreset"
          >
            📋 Пресет для нарядчика
          </button>
          <button
            class="preset-btn minimal-preset"
            title="Мінімальний набір полів"
            @click="applyMinimalPreset"
          >
            📊 Мінімальний вид
          </button>
          <button
            class="preset-btn full-preset"
            title="Повний набір полів"
            @click="applyFullPreset"
          >
            📈 Повний вид
          </button>
        </div>
      </div>

      <div class="actions-section">
        <div class="action-buttons">
          <button
            class="btn-danger"
            title="Скинути всі налаштування до заводських"
            @click="resetAllSettings"
          >
            🔄 Скинути всі налаштування
          </button>
          <button
            class="btn-warning"
            title="Експортувати налаштування"
            @click="exportSettings"
          >
            📤 Експорт
          </button>
          <button
            class="btn-secondary"
            title="Імпортувати налаштування"
            @click="importSettings"
          >
            📥 Імпорт
          </button>
          <button
            class="btn-primary"
            :disabled="!hasUnsavedChanges"
            title="Зберегти всі зміни"
            @click="saveSettings"
          >
            💾 Зберегти зміни
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import { useNotifications } from "@/composables/useNotifications";

const { addNotification } = useNotifications();

// Reactive state
const selectedProfile = ref<string>("dispatcher");
const fieldSearch = ref<string>("");
const hasUnsavedChanges = ref<boolean>(false);

// Available fields definition - fixed list for zanaradka table
const availableFields = ref([
  {
    key: "month",
    label: "Місяць",
    type: "varchar(10)",
    sample_values: ["01", "02", "03"],
  },
  {
    key: "brigade",
    label: "Бригада",
    type: "varchar(50)",
    sample_values: ["Бригада 1", "Бригада 2"],
  },
  {
    key: "shift",
    label: "Зміна",
    type: "varchar(10)",
    sample_values: ["1", "2", "3"],
  },
  {
    key: "route_number",
    label: "Номер маршруту",
    type: "varchar(20)",
    sample_values: ["101", "102", "103"],
  },
  {
    key: "fuel_address",
    label: "Адреса заправки",
    type: "varchar(100)",
    sample_values: ["АЗС-1", "АЗС-2"],
  },
  {
    key: "address",
    label: "Адреса",
    type: "varchar(200)",
    sample_values: ["вул. Центральна, 1", "вул. Головна, 2"],
  },
  {
    key: "route_type",
    label: "Тип маршруту",
    type: "varchar(50)",
    sample_values: ["Міський", "Приміський"],
  },
  {
    key: "internal_number",
    label: "Внутрішній номер",
    type: "varchar(20)",
    sample_values: ["001", "002", "003"],
  },
  {
    key: "driver_name",
    label: "Ім'я водія",
    type: "varchar(100)",
    sample_values: ["Іванов І.І.", "Петров П.П."],
  },
  {
    key: "hour_prep",
    label: "Години підготовки",
    type: "decimal(5,2)",
    sample_values: ["1.5", "2.0", "1.0"],
  },
  {
    key: "hour_work",
    label: "Години роботи",
    type: "decimal(5,2)",
    sample_values: ["8.0", "7.5", "8.5"],
  },
  {
    key: "hour_prep2",
    label: "Години підготовки 2",
    type: "decimal(5,2)",
    sample_values: ["0.5", "1.0", "0.75"],
  },
  {
    key: "hour_work2",
    label: "Години роботи 2",
    type: "decimal(5,2)",
    sample_values: ["4.0", "3.5", "4.5"],
  },
  {
    key: "preparation_time",
    label: "Час підготовки",
    type: "time",
    sample_values: ["07:00", "08:00", "09:00"],
  },
  {
    key: "departure_time",
    label: "Час відправлення",
    type: "time",
    sample_values: ["08:30", "09:30", "10:30"],
  },
  {
    key: "arrival_time",
    label: "Час прибуття",
    type: "time",
    sample_values: ["18:00", "19:00", "20:00"],
  },
  {
    key: "end_time",
    label: "Час закінчення",
    type: "time",
    sample_values: ["19:30", "20:30", "21:30"],
  },
  {
    key: "break_1",
    label: "Перерва 1",
    type: "time",
    sample_values: ["12:00", "13:00", "14:00"],
  },
  {
    key: "break_2",
    label: "Перерва 2",
    type: "time",
    sample_values: ["16:00", "17:00", "18:00"],
  },
  {
    key: "profit_start",
    label: "Початок прибутку",
    type: "time",
    sample_values: ["08:00", "09:00", "10:00"],
  },
  {
    key: "profit_end",
    label: "Кінець прибутку",
    type: "time",
    sample_values: ["18:00", "19:00", "20:00"],
  },
  {
    key: "attendance_place",
    label: "Місце присутності",
    type: "varchar(100)",
    sample_values: ["Депо", "Станція", "Майстерня"],
  },
  {
    key: "finish_place",
    label: "Місце закінчення",
    type: "varchar(100)",
    sample_values: ["Депо", "Станція", "Гараж"],
  },
  {
    key: "parking_place",
    label: "Місце стоянки",
    type: "varchar(100)",
    sample_values: ["Парковка 1", "Парковка 2"],
  },
  {
    key: "vehicle_number",
    label: "Номер транспорту",
    type: "varchar(20)",
    sample_values: ["АА1234АА", "ВВ5678ВВ"],
  },
  {
    key: "waybill_number",
    label: "Номер путівки",
    type: "varchar(50)",
    sample_values: ["001-2024", "002-2024"],
  },
  {
    key: "status",
    label: "Статус",
    type: "varchar(30)",
    sample_values: ["Активний", "Завершений", "Призупинений"],
  },
]);

// Default field configurations - only full view
const defaultFieldConfigs: Record<string, string[]> = {
  dispatcher: [
    "month",
    "brigade",
    "shift",
    "route_number",
    "fuel_address",
    "address",
    "route_type",
    "internal_number",
    "driver_name",
    "hour_prep",
    "hour_work",
    "hour_prep2",
    "hour_work2",
    "preparation_time",
    "departure_time",
    "arrival_time",
    "end_time",
    "break_1",
    "break_2",
    "profit_start",
    "profit_end",
    "attendance_place",
    "finish_place",
    "parking_place",
  ],
  timekeeper_a: [
    "route_number",
    "brigade",
    "shift",
    "driver_name",
    "vehicle_number",
    "departure_time",
    "arrival_time",
    "waybill_number",
    "fuel_address",
    "parking_place",
    "status",
  ],
  timekeeper_b: [
    "route_number",
    "brigade",
    "shift",
    "driver_name",
    "vehicle_number",
    "departure_time",
    "arrival_time",
    "waybill_number",
    "fuel_address",
    "parking_place",
    "status",
  ],
  dispatcher_main: [
    "month",
    "brigade",
    "shift",
    "route_number",
    "fuel_address",
    "address",
    "route_type",
    "internal_number",
    "driver_name",
    "hour_prep",
    "hour_work",
    "hour_prep2",
    "hour_work2",
    "preparation_time",
    "departure_time",
    "arrival_time",
    "end_time",
    "break_1",
    "break_2",
    "profit_start",
    "profit_end",
    "attendance_place",
    "finish_place",
    "parking_place",
  ],
  fuel_accountant: [
    "route_number",
    "brigade",
    "shift",
    "driver_name",
    "vehicle_number",
    "fuel_address",
    "address",
    "departure_time",
    "arrival_time",
    "waybill_number",
    "parking_place",
    "status",
  ],
};

// Current field configurations (loaded from localStorage or defaults)
const fieldConfigs = ref<Record<string, string[]>>({
  dispatcher: [...(defaultFieldConfigs.dispatcher || [])],
  timekeeper_a: [...(defaultFieldConfigs.timekeeper_a || [])],
  timekeeper_b: [...(defaultFieldConfigs.timekeeper_b || [])],
  dispatcher_main: [...(defaultFieldConfigs.dispatcher_main || [])],
  fuel_accountant: [...(defaultFieldConfigs.fuel_accountant || [])],
});

// Computed properties
const selectedFields = computed(() => {
  const fields = fieldConfigs.value[selectedProfile.value];
  if (!Array.isArray(fields) || fields.length === 0) {
    return [...(defaultFieldConfigs[selectedProfile.value] || [])];
  }
  return fields;
});

const filteredAvailableFields = computed(() => {
  const selectedFieldKeys = selectedFields.value || [];

  const filtered = availableFields.value.filter(
    (field) => !selectedFieldKeys.includes(field.key),
  );

  if (fieldSearch.value) {
    return filtered.filter(
      (field) =>
        field.label.toLowerCase().includes(fieldSearch.value.toLowerCase()) ||
        field.key.toLowerCase().includes(fieldSearch.value.toLowerCase()),
    );
  }

  return filtered;
});

// Helper functions
const getProfileDisplayName = (profile: string) => {
  const profileNames: Record<string, string> = {
    dispatcher: "Нарядчик",
    timekeeper_a: "Табельник A",
    timekeeper_b: "Табельник B",
    dispatcher_main: "Диспетчер",
    fuel_accountant: "Бухгалтер з палива",
  };
  return profileNames[profile] || profile;
};

// getTableDisplayName removed - only full view is used

const getFieldLabel = (fieldKey: string) => {
  const field = availableFields.value.find((f) => f.key === fieldKey);
  return field ? field.label : fieldKey;
};

// Field management functions
const addField = (fieldKey: string) => {
  const currentFields = [...selectedFields.value];
  if (!currentFields.includes(fieldKey)) {
    currentFields.push(fieldKey);
    updateCurrentConfiguration(currentFields);
    hasUnsavedChanges.value = true;
  }
};

const removeField = (fieldKey: string) => {
  const currentFields = selectedFields.value.filter((f) => f !== fieldKey);
  updateCurrentConfiguration(currentFields);
  hasUnsavedChanges.value = true;
};

const moveFieldUp = (index: number) => {
  if (index > 0) {
    const currentFields = [...selectedFields.value];
    [currentFields[index], currentFields[index - 1]] = [
      currentFields[index - 1] || "",
      currentFields[index] || "",
    ];
    updateCurrentConfiguration(currentFields);
    hasUnsavedChanges.value = true;
  }
};

const moveFieldDown = (index: number) => {
  if (index < selectedFields.value.length - 1) {
    const currentFields = [...selectedFields.value];
    [currentFields[index], currentFields[index + 1]] = [
      currentFields[index + 1] || "",
      currentFields[index] || "",
    ];
    updateCurrentConfiguration(currentFields);
    hasUnsavedChanges.value = true;
  }
};

const clearAllFields = () => {
  updateCurrentConfiguration([]);
  hasUnsavedChanges.value = true;
};

const updateCurrentConfiguration = (fields: string[]) => {
  fieldConfigs.value[selectedProfile.value] = fields;
};

// Preset functions
const applyDefaultPreset = () => {
  const defaultConfig = defaultFieldConfigs[selectedProfile.value];
  if (defaultConfig) {
    updateCurrentConfiguration([...defaultConfig]);
    hasUnsavedChanges.value = true;
    addNotification({
      type: "success",
      message: "Застосовано стандартні налаштування",
    });
  }
};

const applyDispatcherPreset = () => {
  const dispatcherConfig = defaultFieldConfigs.dispatcher || [];
  updateCurrentConfiguration([...dispatcherConfig]);
  hasUnsavedChanges.value = true;
  addNotification({
    type: "success",
    message: "Застосовано пресет для нарядчика",
  });
};

const applyMinimalPreset = () => {
  const minimalConfig = [
    "route_number",
    "brigade",
    "shift",
    "driver_name",
    "vehicle_number",
    "departure_time",
    "arrival_time",
    "status",
  ];
  updateCurrentConfiguration([...minimalConfig]);
  hasUnsavedChanges.value = true;
  addNotification({
    type: "success",
    message: "Застосовано мінімальний пресет",
  });
};

const applyFullPreset = () => {
  const fullConfig = defaultFieldConfigs.dispatcher || [];
  updateCurrentConfiguration([...fullConfig]);
  hasUnsavedChanges.value = true;
  addNotification({
    type: "success",
    message: "Застосовано повний пресет",
  });
};

// Settings management
const saveSettings = () => {
  // Save to localStorage with profile-specific keys
  Object.keys(fieldConfigs.value).forEach((profile) => {
    const key = `khtrm-admin-field-configs-${profile}`;
    localStorage.setItem(key, JSON.stringify(fieldConfigs.value[profile]));
  });

  // Also save to the main key for backwards compatibility (only full view)
  localStorage.setItem(
    "khtrm-field-configs",
    JSON.stringify({
      full: fieldConfigs.value.dispatcher,
    }),
  );

  hasUnsavedChanges.value = false;
  addNotification({
    type: "success",
    message: "Налаштування збережено для всіх профілів",
  });
};

const resetAllSettings = () => {
  if (
    confirm(
      "Ви впевнені, що хочете скинути всі налаштування? Ця дія незворотня.",
    )
  ) {
    // Clear localStorage
    Object.keys(defaultFieldConfigs).forEach((profile) => {
      const key = `khtrm-admin-field-configs-${profile}`;
      localStorage.removeItem(key);
    });
    localStorage.removeItem("khtrm-field-configs");

    // Reset to defaults
    fieldConfigs.value = {
      dispatcher: [...(defaultFieldConfigs.dispatcher || [])],
      timekeeper_a: [...(defaultFieldConfigs.timekeeper_a || [])],
      timekeeper_b: [...(defaultFieldConfigs.timekeeper_b || [])],
      dispatcher_main: [...(defaultFieldConfigs.dispatcher_main || [])],
      fuel_accountant: [...(defaultFieldConfigs.fuel_accountant || [])],
    };

    hasUnsavedChanges.value = false;
    addNotification({
      type: "success",
      message: "Всі налаштування скинуто до заводських",
    });
  }
};

const exportSettings = () => {
  const settings = {
    version: "1.0",
    timestamp: new Date().toISOString(),
    fieldConfigs: fieldConfigs.value,
  };

  const blob = new Blob([JSON.stringify(settings, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `khtrm-field-settings-${new Date().toISOString().split("T")[0]}.json`;
  a.click();
  URL.revokeObjectURL(url);

  addNotification({
    type: "success",
    message: "Налаштування експортовано",
  });
};

const importSettings = () => {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = ".json";
  input.onchange = (e) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const imported = JSON.parse(e.target?.result as string);
          if (imported.fieldConfigs) {
            fieldConfigs.value = imported.fieldConfigs;
            hasUnsavedChanges.value = true;
            addNotification({
              type: "success",
              message: "Налаштування імпортовано",
            });
          }
        } catch (error) {
          addNotification({
            type: "error",
            message: "Помилка при імпорті налаштувань",
          });
        }
      };
      reader.readAsText(file);
    }
  };
  input.click();
};

const loadSettings = () => {
  // Initialize all profiles with defaults first
  Object.keys(defaultFieldConfigs).forEach((profile) => {
    fieldConfigs.value[profile] = [...(defaultFieldConfigs[profile] || [])];
  });

  // Then try to load saved settings
  Object.keys(defaultFieldConfigs).forEach((profile) => {
    const key = `khtrm-admin-field-configs-${profile}`;
    const saved = localStorage.getItem(key);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) {
          fieldConfigs.value[profile] = parsed;
        }
      } catch (error) {
        // Keep defaults if parsing fails
      }
    }
  });

  hasUnsavedChanges.value = false;
};

// Watch for changes
watch([selectedProfile], () => {
  // Reset field search when switching profiles
  fieldSearch.value = "";
});

// Initialize
onMounted(() => {
  loadSettings();
});
</script>

<style scoped>
.admin-field-settings {
  padding: 20px;
  background: #f8f9fa;
  min-height: 100vh;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.admin-header {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  text-align: center;
}

.admin-header h1 {
  color: #2c3e50;
  margin: 0 0 10px 0;
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.admin-subtitle {
  color: #7f8c8d;
  margin: 0;
  font-size: 1.1rem;
}

.admin-controls {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  display: flex;
  gap: 20px;
  align-items: center;
  flex-wrap: wrap;
}

.database-selector,
.table-selector {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.database-selector label,
.table-selector label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
}

.database-select,
.table-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  min-width: 180px;
}

.loading-indicator {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #3498db;
  background: #f0f8ff;
  border: 1px solid #b3d9ff;
}

.table-fields-info {
  margin-top: 8px;
  padding: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.no-table-selected,
.loading-fields {
  text-align: center;
  padding: 40px 20px;
  color: #7f8c8d;
  font-style: italic;
}

.available-field-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  margin-bottom: 8px;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.available-field-item:hover {
  background: #e8f5e8;
  border-color: #27ae60;
}

.field-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.field-name {
  font-weight: 500;
  color: #2c3e50;
}

.field-type {
  color: #7f8c8d;
  font-size: 0.8rem;
}

.field-samples {
  color: #95a5a6;
  font-size: 0.75rem;
  margin-top: 2px;
}

.database-selector,
.table-selector,
.profile-selector {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.profile-selector {
  margin-left: auto;
}

.database-selector label,
.table-selector label,
.profile-selector label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
}

.database-select,
.table-select,
.profile-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  min-width: 150px;
}

.database-select:disabled,
.table-select:disabled {
  background-color: #f8f9fa;
  color: #6c757d;
  cursor: not-allowed;
}

.save-status {
  margin-left: auto;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.unsaved-indicator {
  color: #e74c3c;
  background: #fdf2f2;
  padding: 8px 16px;
  border-radius: 20px;
  border: 1px solid #fdc2c2;
}

.saved-indicator {
  color: #27ae60;
  background: #f0f9f0;
  padding: 8px 16px;
  border-radius: 20px;
  border: 1px solid #a2d2a2;
}

.settings-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.current-profile-info {
  background: #3498db;
  color: white;
  padding: 20px;
  text-align: center;
}

.current-profile-info h3 {
  margin: 0 0 10px 0;
  font-size: 1.3rem;
}

.profile-name {
  font-weight: 700;
  text-decoration: underline;
}

.table-info {
  margin: 0;
  opacity: 0.9;
}

.database-details {
  margin: 5px 0;
  font-size: 0.95rem;
  opacity: 0.95;
}

.selection-warning {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  padding: 8px 12px;
  margin-top: 8px;
}

.table-fields-info {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  padding: 8px 12px;
  margin-top: 8px;
  font-size: 0.9rem;
}

.field-management {
  padding: 20px;
}

.field-sections {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.selected-fields-section,
.available-fields-section {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.section-header {
  background: #f8f9fa;
  padding: 15px;
  border-bottom: 1px solid #ddd;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-header h4 {
  margin: 0;
  color: #2c3e50;
  font-size: 1rem;
}

.section-actions {
  display: flex;
  gap: 8px;
}

.search-container {
  width: 200px;
}

.field-search {
  width: 100%;
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.selected-fields-list,
.available-fields-list {
  max-height: 400px;
  overflow-y: auto;
  padding: 10px;
}

.selected-field-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  margin-bottom: 8px;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  transition: all 0.2s;
}

.selected-field-item:hover {
  background: #e3f2fd;
  border-color: #3498db;
}

.field-controls {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.move-btn {
  width: 24px;
  height: 20px;
  border: 1px solid #3498db;
  background: white;
  color: #3498db;
  cursor: pointer;
  border-radius: 3px;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.move-btn:hover:not(:disabled) {
  background: #3498db;
  color: white;
}

.move-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.field-label {
  flex: 1;
  font-weight: 500;
  color: #2c3e50;
}

.remove-btn {
  width: 24px;
  height: 24px;
  border: 1px solid #e74c3c;
  background: white;
  color: #e74c3c;
  cursor: pointer;
  border-radius: 50%;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.remove-btn:hover {
  background: #e74c3c;
  color: white;
}

.available-field-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  margin-bottom: 8px;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.available-field-item:hover {
  background: #e8f5e8;
  border-color: #27ae60;
}

.add-btn {
  width: 24px;
  height: 24px;
  border: 1px solid #27ae60;
  background: white;
  color: #27ae60;
  cursor: pointer;
  border-radius: 50%;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.add-btn:hover {
  background: #27ae60;
  color: white;
}

.clear-all-btn {
  padding: 6px 12px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: background 0.2s;
}

.clear-all-btn:hover {
  background: #c0392b;
}

.preset-section {
  background: #f8f9fa;
  padding: 20px;
  border-top: 1px solid #ddd;
}

.preset-section h4 {
  margin: 0 0 15px 0;
  color: #2c3e50;
}

.preset-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.preset-btn {
  padding: 10px 16px;
  border: 1px solid #27ae60;
  background: #2ecc71;
  color: white;
  cursor: pointer;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.preset-btn:hover {
  background: #27ae60;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.actions-section {
  background: #2c3e50;
  padding: 20px;
  border-top: 1px solid #ddd;
}

.action-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary {
  padding: 12px 24px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #2980b9;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  padding: 12px 24px;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #7f8c8d;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.btn-warning {
  padding: 12px 24px;
  background: #f39c12;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
}

.btn-warning:hover {
  background: #e67e22;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.btn-danger {
  padding: 12px 24px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
}

.btn-danger:hover {
  background: #c0392b;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Responsive design */
@media (max-width: 768px) {
  .admin-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .profile-selector {
    flex-direction: row;
    align-items: center;
    margin-left: 0;
  }

  .database-selector,
  .table-selector {
    flex-direction: row;
    align-items: center;
  }

  .field-sections {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .preset-buttons {
    flex-direction: column;
  }
}
</style>
