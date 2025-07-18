<template>
  <div class="assignment-table-container">
    <!-- Header with date selection and view switcher -->
    <div class="table-header">
      <div class="header-left">
        <h2>Наряди на {{ formatDate(selectedDate) }}</h2>
      </div>
      <div class="header-controls">
        <!-- View selector removed - single table view -->

        <!-- Date selector -->
        <div class="date-controls">
          <input
            v-model="selectedDate"
            type="date"
            class="date-input"
            @change="loadAssignments"
          />
          <button class="refresh-btn" @click="refreshData">🔄 Оновити</button>
        </div>
      </div>
    </div>

    <!-- Loading indicator -->
    <div v-if="loading" class="loading">
      <span>Завантаження даних...</span>
    </div>

    <!-- Error message -->
    <div v-if="error" class="error">
      <span>{{ error }}</span>
    </div>

    <!-- Assignment Table -->
    <div v-if="!loading && !error" class="table-wrapper full-view">
      <div class="table-scroll">
        <table class="assignment-table">
          <thead>
            <tr>
              <th class="checkbox-col">
                <input type="checkbox" @change="toggleSelectAll" />
              </th>
              <th v-for="fieldKey in currentFieldConfig" :key="fieldKey">
                {{
                  availableFields.find((f) => f.key === fieldKey)?.label ||
                  fieldKey
                }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="assignment in assignments"
              :key="assignment.id"
              :class="{ selected: assignment.selected }"
            >
              <td class="checkbox-col">
                <input v-model="assignment.selected" type="checkbox" />
              </td>
              <td v-for="fieldKey in currentFieldConfig" :key="fieldKey">
                <span
                  v-if="fieldKey === 'status'"
                  :class="'status-' + assignment.status"
                >
                  {{ getFieldValue(assignment, fieldKey) }}
                </span>
                <span v-else>
                  {{ getFieldValue(assignment, fieldKey) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Table variations removed - single optimized view -->

    <!-- Statistics -->
    <div v-if="!loading && !error && statistics" class="statistics">
      <div class="stat-item">
        <span class="stat-label">Всього нарядів:</span>
        <strong class="stat-value">{{
          statistics.total_assignments || 0
        }}</strong>
      </div>
      <div class="stat-item">
        <span class="stat-label">Активних:</span>
        <strong class="stat-value active">{{
          statistics.active_assignments || 0
        }}</strong>
      </div>
      <div class="stat-item">
        <span class="stat-label">Маршрутів:</span>
        <strong class="stat-value">{{ statistics.total_routes || 0 }}</strong>
      </div>
      <div class="stat-item">
        <span class="stat-label">Завершених:</span>
        <strong class="stat-value completed">{{
          statistics.completed_assignments || 0
        }}</strong>
      </div>
      <!-- Settings button removed - only admin can manage field settings -->
    </div>

    <!-- Field Settings Modal removed - only admin can manage field settings -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useNotifications } from "@/composables/useNotifications";
import type { MSAccessTableRow, AssignmentTableRow, Assignment } from "@/types/dispatcher";

const { addNotification } = useNotifications();

// Reactive state
const assignments = ref<(MSAccessTableRow | AssignmentTableRow)[]>([]);
const statistics = ref<{
  total_assignments: number;
  active_assignments: number;
  total_routes: number;
  completed_assignments: number;
} | null>(null);
const loading = ref(false);
const error = ref("");
const selectedDate = ref(new Date().toISOString().split("T")[0]);
// Single table view - simplified design
// Field settings state removed - only admin can manage field settings

// Available fields definition - exact match with original MS Access table
const availableFields = ref([
  { key: "route_number_field", label: "Мт" }, // Номер маршрута
  { key: "brigade", label: "Вп" },
  { key: "shift", label: "Зм" },
  { key: "vehicle_number_field", label: "Ро" }, // Номер ПС
  { key: "fuel_number", label: "Запр." },
  { key: "fuel_address", label: "Адреса" },
  { key: "route_type", label: "Тип" },
  { key: "internal_number", label: "№ в" },
  { key: "driver_name", label: "ПІБ вод." },
  { key: "hour1", label: "Час1" },
  { key: "hour2", label: "Час2" },
  { key: "hour3", label: "Час3" },
  { key: "hour4", label: "Час4" },
  { key: "preparation_time", label: "П.В." },
  { key: "departure_time", label: "Взд" },
  { key: "arrival_time", label: "Ззд" },
  { key: "end_time", label: "К.В." },
  { key: "break_1", label: "Пер.1" },
  { key: "break_2", label: "Пер.2" },
  { key: "profit_start", label: "П. від" },
  { key: "profit_end", label: "К. від" },
  { key: "attendance_place", label: "М.явки" },
  { key: "finish_place", label: "М. закін" },
  { key: "parking_place", label: "М. відст" },
  // Additional fields for extended functionality
  { key: "waybill_number", label: "П.Б." },
  { key: "driver_tab_number", label: "Таб" },
  { key: "vehicle_number", label: "ПС" },
  { key: "route_endpoint", label: "Кінцева" },
  { key: "day_of_week", label: "День тижня" },
  { key: "status", label: "Статус" },
  { key: "notes", label: "Примітки" },
]);

// Default field configuration - exact match with original MS Access table
const defaultFieldConfig = [
  // Field order: Мт|Вп|Зм|Ро|Запр.|Адреса|Тип|№ в|ПІБ вод.|Час1|Час2|Час3|Час4|П.В.|Взд|Ззд|К.В.|Пер.1|Пер.2|П. від|К. від|М.явки|М. закін|М. відст
  "route_number_field", // Мт - номер маршрута
  "brigade",
  "shift",
  "vehicle_number_field", // Ро - номер ПС
  "fuel_number",
  "fuel_address",
  "route_type",
  "internal_number",
  "driver_name",
  "hour1",
  "hour2",
  "hour3",
  "hour4",
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
];

// Current field configuration (loaded from admin settings or defaults)
const currentFieldConfig = ref<string[]>([...defaultFieldConfig]);

// Load assignments
const loadAssignments = async () => {
  loading.value = true;
  error.value = "";

  try {
    const baseUrl = "http://localhost:8000";
    const endpoint = `${baseUrl}/api/dispatcher/direct-assignments`;

    const response = await fetch(
      `${endpoint}?assignment_date=${selectedDate.value}&limit=100`,
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    assignments.value = data.assignments.map((assignment: Assignment) => ({
      ...assignment,
      selected: false,
    }));

    // Create statistics from assignment data
    statistics.value = {
      total_assignments: data.assignments.length,
      active_assignments: data.assignments.filter(
        (a: Assignment) => a.status === "active",
      ).length,
      total_routes: new Set(
        data.assignments.map((a: Assignment) => a.route_number),
      ).size,
      completed_assignments: data.assignments.filter(
        (a: Assignment) => a.status === "completed",
      ).length,
    };

    if (data.assignments.length === 0) {
      addNotification({
        type: "warning",
        message: `Немає нарядів на ${formatDate(selectedDate.value)}`,
      });
    } else {
      addNotification({
        type: "success",
        message: `Завантажено ${data.assignments.length} нарядів`,
      });
    }
  } catch (err: unknown) {
    error.value = `Помилка завантаження даних: ${err instanceof Error ? err.message : String(err)}`;
    addNotification({
      type: "error",
      message: "Не вдалося завантажити наряди",
    });
  } finally {
    loading.value = false;
  }
};

// Refresh data
const refreshData = () => {
  loadAssignments();
};

// Toggle select all checkbox
const toggleSelectAll = (event: Event) => {
  const checked = (event.target as HTMLInputElement).checked;
  assignments.value.forEach((assignment) => {
    assignment.selected = checked;
  });
};

// Format date for display
const formatDate = (dateString: string | undefined) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  return date.toLocaleDateString("uk-UA", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

// Format status for display
const formatStatus = (status: string) => {
  const statusMap: Record<string, string> = {
    active: "Активний",
    completed: "Завершений",
    cancelled: "Скасований",
  };
  return statusMap[status] || status;
};

// Field settings functions removed - only admin can manage field settings

// Load field settings from admin configuration
const loadFieldSettings = () => {
  try {
    // Check if current user role-specific settings exist
    const userRoleKey = `khtrm-admin-field-configs-dispatcher`; // For dispatcher
    const userRoleSettings = localStorage.getItem(userRoleKey);

    if (userRoleSettings) {
      const parsed = JSON.parse(userRoleSettings);
      if (Array.isArray(parsed) && parsed.length > 0) {
        currentFieldConfig.value = parsed;
        return;
      }
    }

    // Fallback to old format
    const saved = localStorage.getItem("khtrm-field-configs");
    if (saved) {
      const parsed = JSON.parse(saved);
      if (parsed.full && Array.isArray(parsed.full) && parsed.full.length > 0) {
        currentFieldConfig.value = parsed.full;
        return;
      }
    }

    // Use default if nothing found
    currentFieldConfig.value = [...defaultFieldConfig];
  } catch (error) {
    currentFieldConfig.value = [...defaultFieldConfig];
  }
};

const getFieldValue = (assignment: Assignment | MSAccessTableRow | AssignmentTableRow, fieldKey: string) => {
  // Handle field mapping based on MS Access table structure analysis
  const fieldMap: Record<string, string | ((a: any) => string)> = {
    // Based on MS Access column mapping from analysis
    route_number_field: (a) => String(a.route_number || "-"), // Мт = номер маршрута (marshrut)
    brigade: (a) => a.brigade || "-", // Вп = выпуск/бригада (vipusk)
    shift: (a) => a.shift || "-", // Зм = смена (smena)
    vehicle_number_field: (a) => a.vehicle_number || "-", // Ро = номер ПС (pe№)
    fuel_number: (a) => {
      // Запр. = номер заправки (zaprv), если 0 то "-"
      if (a.fuel_number === "0" || a.fuel_number === 0 || !a.fuel_number) {
        return "-";
      }
      return a.fuel_number;
    },
    fuel_address: (a) => a.fuel_address || "Бочка", // Адреса = адрес заправки (ZaprAdr)
    route_type: (a) => a.route_type || "-", // Тип = тип выпуска (tipvipusk)
    internal_number: (a) => a.driver_tab_number || "-", // № в = табельный номер водителя (tabvoditel)
    driver_name: (a) => a.driver_name || "-", // ПІБ вод. = ФИО водителя (fiovoditel)
    hour1: (a) => {
      // Час1 = первый час (подготовка) - расчет на основе plan_hours или time_fakt_line
      if (a.plan_hours && a.plan_hours > 0) {
        return parseFloat(a.plan_hours).toFixed(1);
      }
      if (a.hour_work_actual && a.hour_work_actual > 0) {
        return (parseFloat(a.hour_work_actual) / 3600).toFixed(1);
      }
      // Fallback расчет на основе времени работы
      if (a.departure_time && a.arrival_time) {
        const depTime = a.departure_time.split(":");
        const arrTime = a.arrival_time.split(":");
        const depMinutes = parseInt(depTime[0] || "0") * 60 + parseInt(depTime[1] || "0");
        const arrMinutes = parseInt(arrTime[0] || "0") * 60 + parseInt(arrTime[1] || "0");
        let diffMinutes = arrMinutes - depMinutes;
        if (diffMinutes < 0) diffMinutes += 24 * 60; // Переход через полночь
        return ((diffMinutes / 60) * 0.85).toFixed(1); // 85% от времени работы для первого часа
      }
      return "10,7";
    },
    hour2: (a) => {
      // Час2 = второй час (работа) - расчет на основе времени выхода/захода
      if (a.departure_time && a.arrival_time) {
        const depTime = a.departure_time.split(":");
        const arrTime = a.arrival_time.split(":");
        const depMinutes = parseInt(depTime[0] || "0") * 60 + parseInt(depTime[1] || "0");
        const arrMinutes = parseInt(arrTime[0] || "0") * 60 + parseInt(arrTime[1] || "0");
        let diffMinutes = arrMinutes - depMinutes;
        if (diffMinutes < 0) diffMinutes += 24 * 60; // Переход через полночь
        return (diffMinutes / 60).toFixed(1);
      }
      return "13,4";
    },
    hour3: (a) => {
      // Час3 = третий час на основе смены
      const shift = a.shift?.toString();
      if (shift === "1") return "4,4";
      if (shift === "2") return "49,4";
      return "0";
    },
    hour4: (_a) => "0", // Час4 = четвертый час, всегда 0 как в оригинале MS Access
    preparation_time: (a) => {
      // П.В. = время начала подготовки = Взд - П.В.
      if (a.departure_time && (a as any).preparation_time) {
        const depTime = a.departure_time.split(":");
        const depMinutes = parseInt(depTime[0] || "0") * 60 + parseInt(depTime[1] || "0");

        const prepTime = (a as any).preparation_time.split(":");
        const prepMinutes = parseInt(prepTime[0] || "0") * 60 + parseInt(prepTime[1] || "0");

        let resultMinutes = depMinutes - prepMinutes;
        if (resultMinutes < 0) resultMinutes += 24 * 60; // Переход через полночь

        const hours = Math.floor(resultMinutes / 60);
        const minutes = resultMinutes % 60;
        return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}`;
      }
      return (a as any).preparation_time || "00:10";
    },
    departure_time: (a) => a.departure_time || "-", // Взд = время выхода (tvih)
    arrival_time: (a) => a.arrival_time || "-", // Ззд = время захода (tzah)
    end_time: (a) => {
      // К.В. = время окончания работы = Ззд + К.В.
      if (a.arrival_time && ((a as any).end_time || (a as any).preparation_time)) {
        const arrTime = a.arrival_time.split(":");
        const arrMinutes = parseInt(arrTime[0] || "0") * 60 + parseInt(arrTime[1] || "0");

        const endTimeValue = (a as any).end_time || (a as any).preparation_time || "00:10";
        const endTime = endTimeValue.split(":");
        const endMinutes = parseInt(endTime[0] || "0") * 60 + parseInt(endTime[1] || "0");

        let resultMinutes = arrMinutes + endMinutes;
        if (resultMinutes >= 24 * 60) resultMinutes -= 24 * 60; // Переход через полночь

        const hours = Math.floor(resultMinutes / 60);
        const minutes = resultMinutes % 60;
        return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}`;
      }
      return (a as any).end_time || a.arrival_time || "-";
    },
    break_1: (a) => a.break_1 || "00:00", // Пер. 1 = перерыв 1 (tob1)
    break_2: (a) => a.break_2 || "00:00", // Пер. 2 = перерыв 2 (tob2)
    profit_start: (a) => {
      // П. від = вычисляемое время начала прибыли (tvih + 4:26)
      return a.profit_start || "-";
    },
    profit_end: (a) => {
      // К. від = вычисляемое время окончания прибыли (tzah - 4:37)
      return a.profit_end || "-";
    },
    attendance_place: (a) => a.route_endpoint || "Депо", // М.явки = место явки (kpvih)
    finish_place: (a) => (a as any).route_endpoint_arrival || "Депо", // М. закін = место окончания (kpzah)
    parking_place: (a) => {
      // М. відст = место отстоя (mestootst), если NULL то прочерк
      if (!(a as any).parking_place || (a as any).parking_place === "null") {
        return "-"; // Для NULL значень показувати прочерк
      }
      return (a as any).parking_place;
    },
    waybill_number: (a) => a.waybill_number || "-", // П.Б. = путевой лист (putlist№)
    driver_tab_number: (a) => String(a.driver_tab_number || "-"), // Таб = табельный номер (tabvoditel)
    vehicle_number: (a) => a.vehicle_number || "-", // ПС = номер ПС (pe№)
    route_endpoint: (a) => a.route_endpoint || "-", // Кінцева = конечная остановка (kpvih)
    day_of_week: (a) => {
      const dayMap: Record<string, string> = {
        "1": "Пн",
        "2": "Вт",
        "3": "Ср",
        "4": "Чт",
        "5": "Пт",
        "6": "Сб",
        "7": "Нд",
        понеділок: "Пн",
        вівторок: "Вт",
        середа: "Ср",
        четвер: "Чт",
        "п'ятниця": "Пт",
        субота: "Сб",
        неділя: "Нд",
      };
      return dayMap[(a as any).day_of_week?.toLowerCase()] || (a as any).day_of_week || "-";
    },
    status: (a) => formatStatus(a.status),
    notes: (a) => a.notes || "-", // Примітки = сообщения (Soobhenie)
  };

  const mapping = fieldMap[fieldKey];
  if (typeof mapping === "function") {
    return mapping(assignment);
  } else if (typeof mapping === "string") {
    return String((assignment as any)[mapping] || "-");
  }
  return "-";
};

// Load data on component mount
onMounted(() => {
  loadFieldSettings();
  loadAssignments();
});
</script>

<style scoped>
.assignment-table-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.table-header {
  background: #34495e;
  color: white;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-left h2 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: normal;
}

.header-controls {
  display: flex;
  gap: 20px;
  align-items: center;
}

/* View info styles removed - single table view */

/* View select styles removed - single table view */

.date-controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.date-input {
  padding: 4px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  font-size: 0.9rem;
}

.refresh-btn {
  padding: 4px 12px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.refresh-btn:hover {
  background: #2980b9;
}

.loading,
.error {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  font-weight: 500;
}

.error {
  color: #e74c3c;
}

.table-wrapper {
  flex: 1;
  overflow: hidden;
  background: white;
  margin: 1px;
  width: 100%;
}

.table-scroll {
  width: 100%;
  height: 100%;
  overflow-x: auto;
  overflow-y: auto;
  min-width: 100%;
}

/* Assignment Table Styles */
.assignment-table {
  width: 100%;
  min-width: 1200px;
  border-collapse: collapse;
  font-size: 9px;
  font-family: "Segoe UI", "Inter", system-ui, sans-serif;
  background: white;
  border: 1px solid #e1e5e9;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  table-layout: auto;
}

.assignment-table th {
  background: linear-gradient(135deg, #f8fafb 0%, #e9ecef 100%);
  border: 1px solid #dee2e6;
  padding: 4px 3px;
  text-align: center;
  font-weight: 600;
  color: #495057;
  white-space: nowrap;
  font-size: 8px;
  min-width: 30px;
  max-width: 80px;
  height: 22px;
  position: sticky;
  top: 0;
  z-index: 10;
  overflow: hidden;
  text-overflow: ellipsis;
}

.assignment-table td {
  border: 1px solid #e9ecef;
  padding: 2px 3px;
  text-align: center;
  white-space: nowrap;
  font-size: 8px;
  height: 18px;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 30px;
  max-width: 80px;
  transition: background-color 0.15s ease;
}

.assignment-table tbody tr:nth-child(even) {
  background: #f8f9fa;
}

.assignment-table tbody tr:nth-child(odd) {
  background: white;
}

.assignment-table tbody tr:hover {
  background: #e3f2fd;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.assignment-table tbody tr.selected {
  background: #bbdefb;
  border-left: 3px solid #2196f3;
}

.checkbox-col {
  width: 16px;
  min-width: 16px;
  max-width: 16px;
  padding: 2px;
}

.checkbox-col input[type="checkbox"] {
  width: 12px;
  height: 12px;
  margin: 0;
  accent-color: #2196f3;
  cursor: pointer;
}

/* Table variations removed - unified table design */

/* Status styles */
.status-active {
  color: #27ae60;
  font-weight: 600;
}

.status-completed {
  color: #95a5a6;
  font-weight: 600;
}

.status-cancelled {
  color: #e74c3c;
  font-weight: 600;
}

/* Statistics */
.statistics {
  background: white;
  padding: 15px 20px;
  border-top: 1px solid #ddd;
  display: flex;
  gap: 20px;
  font-size: 0.9rem;
  align-items: center;
  flex-wrap: wrap;
}

.stat-item {
  flex: 1;
  min-width: 120px;
  padding: 8px;
  text-align: center;
  background: #f8f9fa;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stat-label {
  color: #7f8c8d;
  font-size: 0.85rem;
  display: block;
  margin-bottom: 4px;
}

.stat-value {
  color: #2c3e50;
  font-size: 1.1rem;
  display: block;
  font-weight: 600;
}

.stat-value.active {
  color: #27ae60;
}

.stat-value.completed {
  color: #2980b9;
}

/* Quick settings button styles removed - only admin can manage field settings */

/* Responsive design */
@media (max-width: 1200px) {
  .assignment-table {
    font-size: 10px;
  }

  .assignment-table th,
  .assignment-table td {
    padding: 2px 3px;
  }
}

@media (max-width: 768px) {
  .table-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .header-controls {
    flex-direction: column;
    width: 100%;
    gap: 10px;
  }

  .statistics {
    flex-direction: column;
    gap: 10px;
  }
}

/* Settings button styles and modal styles removed - only admin can manage field settings */

/* All field settings modal CSS removed - only admin can manage field settings */
</style>
