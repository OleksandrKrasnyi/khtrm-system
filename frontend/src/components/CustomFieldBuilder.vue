<template>
  <div class="custom-field-builder">
    <div class="builder-header">
      <h3>
        <i :class="props.editingField ? 'fas fa-edit' : 'fas fa-plus-circle'" />
        {{ props.editingField ? 'Редагувати кастомне поле' : 'Створити кастомне поле' }}
      </h3>
      <button class="close-btn" @click="$emit('close')">
        <i class="fas fa-times" />
      </button>
    </div>

    <div class="builder-content">
      <!-- Field Type Selection -->
      <div class="field-type-selection">
        <h4>Тип поля:</h4>
        <div class="field-types">
          <div
            v-for="type in fieldTypes"
            :key="type.id"
            class="field-type-card"
            :class="{ active: selectedType === type.id }"
            @click="selectFieldType(type.id)"
          >
            <div class="type-icon">
              <i :class="type.icon" />
            </div>
            <div class="type-info">
              <h5>{{ type.name }}</h5>
              <p>{{ type.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Field Configuration -->
      <div v-if="selectedType" class="field-configuration">
        <div class="config-header">
          <h4>Налаштування поля</h4>
        </div>

        <!-- Basic Field Info -->
        <div class="basic-config">
          <div class="form-group">
            <label>Назва поля:</label>
            <input
              v-model="fieldConfig.name"
              type="text"
              placeholder="Введіть назву поля"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label>Мітка для відображення:</label>
            <input
              v-model="fieldConfig.label"
              type="text"
              placeholder="Як буде показуватися в таблиці"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label>Опис:</label>
            <textarea
              v-model="fieldConfig.description"
              placeholder="Опис поля (необов'язково)"
              class="form-textarea"
              rows="2"
            />
          </div>
        </div>

        <!-- Type-specific Configuration -->
        <div class="type-specific-config">
          <!-- Calculated Field -->
          <div v-if="selectedType === 'calculated'" class="calculated-config">
            <h5>Конфігурація обчислюваного поля</h5>
            
            <div class="form-group">
              <label>Тип обчислення:</label>
              <select v-model="fieldConfig.calculationType" class="form-select">
                <option value="time_difference">Різниця часу</option>
                <option value="date_difference">Різниця дат</option>
                <option value="arithmetic">Арифметичні операції</option>
                <option value="concatenation">Об'єднання полів</option>
                <option value="conditional">Умовна логіка</option>
              </select>
            </div>

            <!-- Time Difference -->
            <div v-if="fieldConfig.calculationType === 'time_difference'" class="time-diff-config">
              <div class="form-group">
                <label>Поле початкового часу:</label>
                <select v-model="fieldConfig.startTimeField" class="form-select">
                  <option value="">Виберіть поле</option>
                  <option v-for="field in timeStringFields" :key="field.name" :value="field.name">
                    {{ field.name }} ({{ field.type }})
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label>Поле кінцевого часу:</label>
                <select v-model="fieldConfig.endTimeField" class="form-select">
                  <option value="">Виберіть поле</option>
                  <option v-for="field in timeStringFields" :key="field.name" :value="field.name">
                    {{ field.name }} ({{ field.type }})
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label>Формат результату:</label>
                <select v-model="fieldConfig.resultFormat" class="form-select">
                  <option value="minutes">Хвилини (число)</option>
                  <option value="hours_minutes">Години:Хвилини (HH:MM)</option>
                  <option value="decimal_hours">Години (десятковий дріб)</option>
                </select>
              </div>

              <div class="info-box">
                <i class="fas fa-info-circle"></i>
                <p>Підтримуються поля varchar(5) з часом у форматі HH:MM (наприклад: 05:55, 19:42)</p>
              </div>
            </div>

            <!-- Date Difference -->
            <div v-if="fieldConfig.calculationType === 'date_difference'" class="date-diff-config">
              <div class="form-group">
                <label>Поле початкової дати:</label>
                <select v-model="fieldConfig.startDateField" class="form-select">
                  <option value="">Виберіть поле</option>
                  <option v-for="field in dateFields" :key="field.name" :value="field.name">
                    {{ field.name }} ({{ field.type }})
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label>Поле кінцевої дати:</label>
                <select v-model="fieldConfig.endDateField" class="form-select">
                  <option value="">Виберіть поле</option>
                  <option v-for="field in dateFields" :key="field.name" :value="field.name">
                    {{ field.name }} ({{ field.type }})
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label>Одиниця вимірювання:</label>
                <select v-model="fieldConfig.dateUnit" class="form-select">
                  <option value="days">Дні</option>
                  <option value="weeks">Тижні</option>
                  <option value="months">Місяці</option>
                </select>
              </div>
            </div>

            <!-- Arithmetic Operations -->
            <div v-if="fieldConfig.calculationType === 'arithmetic'" class="arithmetic-config">
              <div class="form-group">
                <label>Формула:</label>
                <div class="formula-builder">
                  <div class="formula-input">
                    <input
                      v-model="fieldConfig.formula"
                      type="text"
                      placeholder="Наприклад: {field1} + {field2} * 2"
                      class="form-input"
                    />
                  </div>
                  <div class="available-fields">
                    <h6>Доступні поля:</h6>
                    <div class="field-tags">
                      <span
                        v-for="field in numericFields"
                        :key="field.name"
                        class="field-tag"
                        @click="addFieldToFormula(field.name)"
                      >
                        {{ field.name }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Concatenation -->
            <div v-if="fieldConfig.calculationType === 'concatenation'" class="concat-config">
              <div class="form-group">
                <label>Поля для об'єднання:</label>
                <div class="field-selection">
                  <div
                    v-for="field in availableFields"
                    :key="field.name"
                    class="field-checkbox"
                  >
                    <input
                      :id="'concat-' + field.name"
                      v-model="fieldConfig.concatFields"
                      type="checkbox"
                      :value="field.name"
                    />
                    <label :for="'concat-' + field.name">{{ field.name }}</label>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label>Розділювач:</label>
                <input
                  v-model="fieldConfig.separator"
                  type="text"
                  placeholder="Наприклад: ', ' або ' - '"
                  class="form-input"
                />
              </div>
            </div>

            <!-- Conditional Logic -->
            <div v-if="fieldConfig.calculationType === 'conditional'" class="conditional-config">
              <div class="form-group">
                <label>Умова:</label>
                <select v-model="fieldConfig.conditionField" class="form-select">
                  <option value="">Виберіть поле</option>
                  <option v-for="field in availableFields" :key="field.name" :value="field.name">
                    {{ field.name }} ({{ field.type }})
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label>Оператор:</label>
                <select v-model="fieldConfig.conditionOperator" class="form-select">
                  <option value="equals">Дорівнює</option>
                  <option value="not_equals">Не дорівнює</option>
                  <option value="greater">Більше</option>
                  <option value="less">Менше</option>
                  <option value="contains">Містить</option>
                  <option value="not_contains">Не містить</option>
                </select>
              </div>

              <div class="form-group">
                <label>Значення:</label>
                <input
                  v-model="fieldConfig.conditionValue"
                  type="text"
                  placeholder="Значення для порівняння"
                  class="form-input"
                />
              </div>

              <div class="form-group">
                <label>Значення при true:</label>
                <input
                  v-model="fieldConfig.trueValue"
                  type="text"
                  placeholder="Що показати якщо умова виконується"
                  class="form-input"
                />
              </div>

              <div class="form-group">
                <label>Значення при false:</label>
                <input
                  v-model="fieldConfig.falseValue"
                  type="text"
                  placeholder="Що показати якщо умова не виконується"
                  class="form-input"
                />
              </div>
            </div>
          </div>

          <!-- Join Field -->
          <div v-if="selectedType === 'join'" class="join-config">
            <h5>Конфігурація поля з об'єднанням</h5>
            
            <div class="form-group">
              <label>Цільова таблиця:</label>
              <select v-model="fieldConfig.joinTable" class="form-select" @change="loadJoinTableFields">
                <option value="">Виберіть таблицю</option>
                <option v-for="table in availableTables" :key="table.name" :value="table.name">
                  {{ table.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Поле для об'єднання (поточна таблиця):</label>
              <select v-model="fieldConfig.joinSourceField" class="form-select">
                <option value="">Виберіть поле</option>
                <option v-for="field in availableFields" :key="field.name" :value="field.name">
                  {{ field.name }} ({{ field.type }})
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Поле для об'єднання (цільова таблиця):</label>
              <select v-model="fieldConfig.joinTargetField" class="form-select">
                <option value="">Виберіть поле</option>
                <option v-for="field in joinTableFields" :key="field.name" :value="field.name">
                  {{ field.name }} ({{ field.type }})
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Поле для відображення:</label>
              <select v-model="fieldConfig.joinDisplayField" class="form-select">
                <option value="">Виберіть поле</option>
                <option v-for="field in joinTableFields" :key="field.name" :value="field.name">
                  {{ field.name }} ({{ field.type }})
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Тип об'єднання:</label>
              <select v-model="fieldConfig.joinType" class="form-select">
                <option value="LEFT">LEFT JOIN</option>
                <option value="INNER">INNER JOIN</option>
                <option value="RIGHT">RIGHT JOIN</option>
              </select>
            </div>
          </div>

          <!-- Aggregate Field -->
          <div v-if="selectedType === 'aggregate'" class="aggregate-config">
            <h5>Конфігурація агрегатного поля</h5>
            
            <div class="form-group">
              <label>Функція агрегації:</label>
              <select v-model="fieldConfig.aggregateFunction" class="form-select">
                <option value="COUNT">Кількість</option>
                <option value="SUM">Сума</option>
                <option value="AVG">Середнє</option>
                <option value="MIN">Мінімум</option>
                <option value="MAX">Максимум</option>
              </select>
            </div>

            <div class="form-group">
              <label>Поле для агрегації:</label>
              <select v-model="fieldConfig.aggregateField" class="form-select">
                <option value="">Виберіть поле</option>
                <option v-for="field in numericFields" :key="field.name" :value="field.name">
                  {{ field.name }} ({{ field.type }})
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Групування за:</label>
              <select v-model="fieldConfig.groupByField" class="form-select">
                <option value="">Без групування</option>
                <option v-for="field in availableFields" :key="field.name" :value="field.name">
                  {{ field.name }} ({{ field.type }})
                </option>
              </select>
            </div>
          </div>

          <!-- Lookup Field -->
          <div v-if="selectedType === 'lookup'" class="lookup-config">
            <h5>Конфігурація поля пошуку</h5>
            
            <div class="form-group">
              <label>Таблиця довідника:</label>
              <select v-model="fieldConfig.lookupTable" class="form-select" @change="loadLookupTableFields">
                <option value="">Виберіть таблицю</option>
                <option v-for="table in availableTables" :key="table.name" :value="table.name">
                  {{ table.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Поле для пошуку:</label>
              <select v-model="fieldConfig.lookupKeyField" class="form-select">
                <option value="">Виберіть поле</option>
                <option v-for="field in availableFields" :key="field.name" :value="field.name">
                  {{ field.name }} ({{ field.type }})
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Поле довідника для пошуку:</label>
              <select v-model="fieldConfig.lookupSearchField" class="form-select">
                <option value="">Виберіть поле</option>
                <option v-for="field in lookupTableFields" :key="field.name" :value="field.name">
                  {{ field.name }} ({{ field.type }})
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Поле для відображення:</label>
              <select v-model="fieldConfig.lookupDisplayField" class="form-select">
                <option value="">Виберіть поле</option>
                <option v-for="field in lookupTableFields" :key="field.name" :value="field.name">
                  {{ field.name }} ({{ field.type }})
                </option>
              </select>
            </div>
          </div>
        </div>

        <!-- Preview -->
        <div v-if="canPreview" class="field-preview">
          <h5>Превью поля</h5>
          <div class="preview-content">
            <div class="preview-header">
              <strong>{{ fieldConfig.label || fieldConfig.name }}</strong>
              <span class="preview-type">({{ getSelectedTypeName() }})</span>
            </div>
            <div class="preview-description">
              {{ fieldConfig.description || 'Опис відсутній' }}
            </div>
            <div class="preview-sql">
              <h6>SQL запит:</h6>
              <pre>{{ generateSQLPreview() }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="builder-actions">
      <button class="btn-secondary" @click="$emit('close')">
        <i class="fas fa-times" />
        Скасувати
      </button>
      <button
        :disabled="!canSave"
        class="btn-primary"
        @click="saveCustomField"
      >
        <i class="fas fa-save" />
        {{ props.editingField ? 'Оновити поле' : 'Зберегти поле' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useNotifications } from '@/composables/useNotifications';

const { addNotification } = useNotifications();

// Define component options for proper TypeScript support
defineOptions({
  name: 'CustomFieldBuilder'
});

// Props
const props = defineProps<{
  availableFields: Array<{
    name: string;
    type: string;
    is_key?: boolean;
  }>;
  availableTables: Array<{
    name: string;
    row_count: number;
  }>;
  database: string;
  sourceTable: string;
  editingField?: CustomField | null;
}>();

// Emits
const emit = defineEmits<{
  close: [];
  save: [field: CustomField];
}>();

// Types
interface CustomField {
  id: string;
  name: string;
  label: string;
  type: string;
  description?: string;
  config: Record<string, unknown>;
  sql?: string;
}

interface FieldType {
  id: string;
  name: string;
  description: string;
  icon: string;
}

interface FieldConfig {
  name: string;
  label: string;
  description: string;
  calculationType: string;
  resultFormat: string;
  dateUnit: string;
  formula: string;
  concatFields: string[];
  separator: string;
  conditionOperator: string;
  joinType: string;
  aggregateFunction: string;
  [key: string]: unknown;
}

// Reactive state
const selectedType = ref<string>('');
const fieldConfig = ref<FieldConfig>({
  name: '',
  label: '',
  description: '',
  calculationType: 'time_difference',
  resultFormat: 'minutes',
  dateUnit: 'days',
  formula: '',
  concatFields: [],
  separator: ', ',
  conditionOperator: 'equals',
  joinType: 'LEFT',
  aggregateFunction: 'COUNT',
});

const joinTableFields = ref<Array<{ name: string; type: string }>>([]);
const lookupTableFields = ref<Array<{ name: string; type: string }>>([]);

// Field types configuration
const fieldTypes: FieldType[] = [
  {
    id: 'calculated',
    name: 'Обчислюване поле',
    description: 'Поле з розрахунками на основі інших полів',
    icon: 'fas fa-calculator'
  },
  {
    id: 'join',
    name: 'Об\'єднання таблиць',
    description: 'Поле з даними з іншої таблиці через JOIN',
    icon: 'fas fa-link'
  },
  {
    id: 'aggregate',
    name: 'Агрегатне поле',
    description: 'Поле з агрегатними функціями (SUM, COUNT, тощо)',
    icon: 'fas fa-chart-bar'
  },
  {
    id: 'lookup',
    name: 'Поле пошуку',
    description: 'Поле для пошуку значень у довіднику',
    icon: 'fas fa-search'
  }
];

// Computed properties
const timeStringFields = computed(() => {
  return props.availableFields.filter(field => {
    const type = field.type.toLowerCase();
    // Check for varchar(5) specifically for HH:MM format
    return type.includes('varchar(5)') || 
           type.includes('char(5)') ||
           type.includes('time') || 
           type.includes('datetime');
  });
});

const dateFields = computed(() => {
  return props.availableFields.filter(field => 
    field.type.toLowerCase().includes('date') || 
    field.type.toLowerCase().includes('datetime')
  );
});

const numericFields = computed(() => {
  return props.availableFields.filter(field => 
    field.type.toLowerCase().includes('int') || 
    field.type.toLowerCase().includes('decimal') || 
    field.type.toLowerCase().includes('float') ||
    field.type.toLowerCase().includes('double')
  );
});

const canPreview = computed(() => {
  return selectedType.value && fieldConfig.value.name && fieldConfig.value.label;
});

const canSave = computed(() => {
  if (!selectedType.value || !fieldConfig.value.name || !fieldConfig.value.label) {
    return false;
  }

  switch (selectedType.value) {
    case 'calculated':
      return validateCalculatedField();
    case 'join':
      return validateJoinField();
    case 'aggregate':
      return validateAggregateField();
    case 'lookup':
      return validateLookupField();
    default:
      return false;
  }
});

// Methods
const selectFieldType = (typeId: string) => {
  selectedType.value = typeId;
  resetFieldConfig();
};

const resetFieldConfig = () => {
  fieldConfig.value = {
    name: '',
    label: '',
    description: '',
    calculationType: 'time_difference',
    resultFormat: 'minutes',
    dateUnit: 'days',
    formula: '',
    concatFields: [],
    separator: ', ',
    conditionOperator: 'equals',
    joinType: 'LEFT',
    aggregateFunction: 'COUNT',
  };
};

const addFieldToFormula = (fieldName: string) => {
  fieldConfig.value.formula += `{${fieldName}}`;
};

const loadJoinTableFields = async () => {
  if (!fieldConfig.value.joinTable) return;
  
  try {
    const response = await fetch(
      `http://localhost:8000/api/dispatcher/admin/table-fields?database_name=${props.database}&table_name=${fieldConfig.value.joinTable}`
    );
    if (!response.ok) throw new Error('Failed to load join table fields');
    
    const data = await response.json();
    joinTableFields.value = data.fields;
  } catch (error) {
    console.error('Error loading join table fields:', error);
    addNotification({
      type: 'error',
      message: 'Помилка завантаження полів таблиці'
    });
  }
};

const loadLookupTableFields = async () => {
  if (!fieldConfig.value.lookupTable) return;
  
  try {
    const response = await fetch(
      `http://localhost:8000/api/dispatcher/admin/table-fields?database_name=${props.database}&table_name=${fieldConfig.value.lookupTable}`
    );
    if (!response.ok) throw new Error('Failed to load lookup table fields');
    
    const data = await response.json();
    lookupTableFields.value = data.fields;
  } catch (error) {
    console.error('Error loading lookup table fields:', error);
    addNotification({
      type: 'error',
      message: 'Помилка завантаження полів довідника'
    });
  }
};

const validateCalculatedField = (): boolean => {
  switch (fieldConfig.value.calculationType) {
    case 'time_difference':
      return !!(fieldConfig.value.startTimeField && fieldConfig.value.endTimeField && fieldConfig.value.resultFormat);
    case 'date_difference':
      return !!(fieldConfig.value.startDateField && fieldConfig.value.endDateField);
    case 'arithmetic':
      return !!fieldConfig.value.formula;
    case 'concatenation':
      return fieldConfig.value.concatFields.length > 0;
    case 'conditional':
      return !!(fieldConfig.value.conditionField && fieldConfig.value.conditionOperator);
    default:
      return false;
  }
};

const validateJoinField = (): boolean => {
  return !!(
    fieldConfig.value.joinTable &&
    fieldConfig.value.joinSourceField &&
    fieldConfig.value.joinTargetField &&
    fieldConfig.value.joinDisplayField
  );
};

const validateAggregateField = (): boolean => {
  return !!(fieldConfig.value.aggregateFunction && fieldConfig.value.aggregateField);
};

const validateLookupField = (): boolean => {
  return !!(
    fieldConfig.value.lookupTable &&
    fieldConfig.value.lookupKeyField &&
    fieldConfig.value.lookupSearchField &&
    fieldConfig.value.lookupDisplayField
  );
};

const getSelectedTypeName = (): string => {
  const type = fieldTypes.find(t => t.id === selectedType.value);
  return type ? type.name : '';
};

const generateSQLPreview = (): string => {
  if (!selectedType.value) return '';

  switch (selectedType.value) {
    case 'calculated':
      return generateCalculatedSQL();
    case 'join':
      return generateJoinSQL();
    case 'aggregate':
      return generateAggregateSQL();
    case 'lookup':
      return generateLookupSQL();
    default:
      return '';
  }
};

const generateCalculatedSQL = (): string => {
  switch (fieldConfig.value.calculationType) {
    case 'time_difference': {
      const format = fieldConfig.value.resultFormat;
      const startField = fieldConfig.value.startTimeField;
      const endField = fieldConfig.value.endTimeField;
      
      if (format === 'minutes') {
        return `(TIME_TO_SEC(${endField}) - TIME_TO_SEC(${startField})) / 60 AS ${fieldConfig.value.name}`;
      } else if (format === 'hours_minutes') {
        return `TIME_FORMAT(SEC_TO_TIME(TIME_TO_SEC(${endField}) - TIME_TO_SEC(${startField})), '%H:%i') AS ${fieldConfig.value.name}`;
      } else if (format === 'decimal_hours') {
        return `(TIME_TO_SEC(${endField}) - TIME_TO_SEC(${startField})) / 3600 AS ${fieldConfig.value.name}`;
      }
      return '';
    }
    case 'date_difference':
      return `DATEDIFF(${fieldConfig.value.endDateField}, ${fieldConfig.value.startDateField}) AS ${fieldConfig.value.name}`;
    case 'arithmetic':
      return `(${fieldConfig.value.formula.replace(/\{(\w+)\}/g, '$1')}) AS ${fieldConfig.value.name}`;
    case 'concatenation':
      return `CONCAT(${fieldConfig.value.concatFields.join(`, '${fieldConfig.value.separator}', `)}) AS ${fieldConfig.value.name}`;
    case 'conditional':
      return `CASE WHEN ${fieldConfig.value.conditionField} ${getOperatorSQL(fieldConfig.value.conditionOperator)} '${fieldConfig.value.conditionValue}' THEN '${fieldConfig.value.trueValue}' ELSE '${fieldConfig.value.falseValue}' END AS ${fieldConfig.value.name}`;
    default:
      return '';
  }
};

const generateJoinSQL = (): string => {
  return `${fieldConfig.value.joinTable}.${fieldConfig.value.joinDisplayField} AS ${fieldConfig.value.name}`;
};

const generateAggregateSQL = (): string => {
  const groupBy = fieldConfig.value.groupByField ? ` GROUP BY ${fieldConfig.value.groupByField}` : '';
  return `${fieldConfig.value.aggregateFunction}(${fieldConfig.value.aggregateField}) AS ${fieldConfig.value.name}${groupBy}`;
};

const generateLookupSQL = (): string => {
  return `lookup_table.${fieldConfig.value.lookupDisplayField} AS ${fieldConfig.value.name}`;
};

const getOperatorSQL = (operator: string): string => {
  switch (operator) {
    case 'equals': return '=';
    case 'not_equals': return '!=';
    case 'greater': return '>';
    case 'less': return '<';
    case 'contains': return 'LIKE';
    case 'not_contains': return 'NOT LIKE';
    default: return '=';
  }
};

const saveCustomField = () => {
  if (!canSave.value) return;

  const customField: CustomField = {
    id: Date.now().toString(),
    name: fieldConfig.value.name,
    label: fieldConfig.value.label,
    type: selectedType.value,
    description: fieldConfig.value.description,
    config: { ...fieldConfig.value },
    sql: generateSQLPreview()
  };

  emit('save', customField);
  addNotification({
    type: 'success',
    message: `Кастомне поле "${customField.label}" створено!`
  });
};

// Watch for name changes to auto-fill label
watch(() => fieldConfig.value.name, (newName) => {
  if (newName && !fieldConfig.value.label) {
    fieldConfig.value.label = newName;
  }
});

// Initialize with editing field if provided
watch(() => props.editingField, (editingField) => {
  if (editingField) {
    selectedType.value = editingField.type;
    fieldConfig.value = {
      name: editingField.name,
      label: editingField.label,
      description: editingField.description || '',
      calculationType: 'time_difference',
      resultFormat: 'minutes',
      dateUnit: 'days',
      formula: '',
      concatFields: [],
      separator: ', ',
      conditionOperator: 'equals',
      joinType: 'LEFT',
      aggregateFunction: 'COUNT',
      ...editingField.config
    };
  }
}, { immediate: true });

// Component name is already defined above
</script>

<style scoped>
.custom-field-builder {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.builder-header {
  padding: 20px 25px;
  border-bottom: 1px solid #e1e8ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8f9fa;
}

.builder-header h3 {
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

.builder-content {
  flex: 1;
  overflow-y: auto;
  padding: 25px;
}

.field-type-selection h4 {
  color: #2c3e50;
  margin: 0 0 15px 0;
  font-size: 1.1rem;
}

.field-types {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.field-type-card {
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 15px;
}

.field-type-card:hover {
  border-color: #3498db;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.field-type-card.active {
  border-color: #3498db;
  background: #e8f4f8;
}

.type-icon {
  font-size: 2rem;
  color: #3498db;
  width: 40px;
  text-align: center;
}

.type-info h5 {
  margin: 0 0 5px 0;
  color: #2c3e50;
  font-size: 1rem;
}

.type-info p {
  margin: 0;
  color: #7f8c8d;
  font-size: 0.9rem;
  line-height: 1.3;
}

.field-configuration {
  border-top: 1px solid #e1e8ed;
  padding-top: 25px;
}

.config-header h4 {
  color: #2c3e50;
  margin: 0 0 20px 0;
  font-size: 1.1rem;
}

.basic-config {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.type-specific-config {
  background: #fff;
  border: 1px solid #e1e8ed;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.type-specific-config h5 {
  color: #2c3e50;
  margin: 0 0 15px 0;
  font-size: 1rem;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #2c3e50;
  font-weight: 600;
  font-size: 0.9rem;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #e1e8ed;
  border-radius: 6px;
  font-size: 0.9rem;
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
  min-height: 60px;
}

.formula-builder {
  border: 1px solid #e1e8ed;
  border-radius: 6px;
  padding: 15px;
  background: #f8f9fa;
}

.formula-input {
  margin-bottom: 15px;
}

.available-fields h6 {
  color: #2c3e50;
  margin: 0 0 10px 0;
  font-size: 0.9rem;
}

.field-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.field-tag {
  background: #3498db;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.field-tag:hover {
  background: #2980b9;
}

.field-selection {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
  border: 1px solid #e1e8ed;
  border-radius: 6px;
  padding: 15px;
  background: #f8f9fa;
}

.field-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
}

.field-checkbox input {
  width: auto;
}

.field-checkbox label {
  margin: 0;
  font-weight: normal;
  cursor: pointer;
}

.field-preview {
  background: #f8f9fa;
  border: 1px solid #e1e8ed;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.field-preview h5 {
  color: #2c3e50;
  margin: 0 0 15px 0;
  font-size: 1rem;
}

.preview-content {
  background: white;
  border-radius: 6px;
  padding: 15px;
}

.preview-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.preview-header strong {
  color: #2c3e50;
}

.preview-type {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.preview-description {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-bottom: 15px;
}

.preview-sql h6 {
  color: #2c3e50;
  margin: 0 0 8px 0;
  font-size: 0.9rem;
}

.preview-sql pre {
  background: #2c3e50;
  color: #ecf0f1;
  padding: 10px;
  border-radius: 4px;
  font-size: 0.8rem;
  overflow-x: auto;
  margin: 0;
}

.builder-actions {
  padding: 20px 25px;
  border-top: 1px solid #e1e8ed;
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  background: #f8f9fa;
}

.btn-primary,
.btn-secondary {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
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

/* Info box */
.info-box {
  background: #e8f4f8;
  border: 1px solid #3498db;
  border-radius: 6px;
  padding: 12px;
  margin-top: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.info-box i {
  color: #3498db;
  font-size: 1.1rem;
}

.info-box p {
  margin: 0;
  color: #2c3e50;
  font-size: 0.9rem;
  line-height: 1.4;
}

/* Responsive design */
@media (max-width: 768px) {
  .custom-field-builder {
    max-width: 95vw;
    margin: 10px;
  }

  .field-types {
    grid-template-columns: 1fr;
  }

  .field-selection {
    grid-template-columns: 1fr;
  }

  .builder-actions {
    flex-direction: column;
  }
}
</style>