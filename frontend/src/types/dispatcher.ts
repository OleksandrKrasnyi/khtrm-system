/**
 * Enhanced TypeScript interfaces for dispatcher functionality
 * Based on enhanced Assignment model with all MS Access fields
 */

export interface Assignment {
  id: number;

  // Date and time information
  assignment_date: string; // ISO date string - Дата зарядки
  month?: number; // Месяц (Мт)

  // Brigade and shift information
  brigade?: string; // Бригада (Бр)
  shift?: string; // Смена
  shift_display?: string; // Human readable shift

  // Application and address
  application_number?: string; // Заявка
  address?: string; // Адрес

  // Route and type information
  route_number: number; // Номер маршрута
  route_type?: string; // Тип
  internal_number?: string; // № в

  // Fuel information
  fuel_route?: string; // Маршрут топливо
  fuel_address?: string; // Адрес заправки

  // Driver waybill information
  driver_waybill?: string; // ПБ вод

  // Working hours (5 different hour periods)
  hour1?: string; // Час1 (HH:mm format)
  hour2?: string; // Час2 (HH:mm format)
  hour3?: string; // Час3 (HH:mm format)
  hour4?: string; // Час4 (HH:mm format)
  hour5?: string; // Час5 (HH:mm format)

  // Waybill and departure information
  waybill_number?: string; // П.Б.
  departure_vzd?: string; // Взд (время выезда) (HH:mm format)
  departure_zgd?: string; // Згд (время заезда) (HH:mm format)

  // End time and shifts
  end_kb?: string; // К.Б. (HH:mm format)
  break_1?: string; // Пер.1 (HH:mm format)
  break_2?: string; // Пер.2 (HH:mm format)

  // Profitability and efficiency
  profit_start?: string; // П.выг (HH:mm format)
  profit_end?: string; // К.выг (HH:mm format)

  // Vehicle information
  vehicle_number?: string; // Н.авт
  vehicle_model?: string; // М.авт
  vehicle_bedt?: string; // М.Бедт

  // Additional information
  coal_info?: string; // Вугл
  vehicle_type_pc?: string; // Тип PC
  state_number_pc?: string; // Держ.№ PC

  // Driver and conductor information
  driver_tab_number?: number; // Табельный номер водителя
  driver_name?: string; // ФИО водителя
  conductor_tab_number?: number; // Табельный номер кондуктора
  conductor_name?: string; // ФИО кондуктора

  // Standard schedule information
  departure_time?: string; // Время выхода (HH:mm format)
  arrival_time?: string; // Время захода (HH:mm format)

  // Route endpoints
  route_endpoint?: string; // Конечная остановка

  // Status and control
  status: string; // Статус наряда
  notes?: string; // Примечания

  // Computed properties
  display_name: string; // Human readable assignment name
  working_hours_summary?: string; // Summary of all working hours
  breaks_summary?: string; // Summary of break periods
  full_vehicle_info?: string; // Complete vehicle information
}

// MS Access table format (for /full-assignments endpoint)
export interface MSAccessAssignment {
  id: number;
  date_charging: string; // Дата зарядки
  month?: number; // Мт
  brigade?: string; // Бр
  application?: string; // Заявка
  address?: string; // Адрес
  type?: string; // Тип
  number_in?: string; // № в
  fuel_route?: string; // Марш топливо
  driver_pb?: string; // ПБ вод
  hour1?: string; // Час1
  hour2?: string; // Час2
  hour3?: string; // Час3
  hour4?: string; // Час4
  hour5?: string; // Час5
  pb?: string; // П.Б.
  vzd?: string; // Взд
  zgd?: string; // Згд
  kb?: string; // К.Б.
  break_1?: string; // Пер.1
  break_2?: string; // Пер.2
  profit_start?: string; // П.выг
  profit_end?: string; // К.выг
  vehicle_number?: string; // Н.авт
  vehicle_model?: string; // М.авт
  vehicle_bedt?: string; // М.Бедт
  coal?: string; // Вугл
  vehicle_type?: string; // Тип PC
  state_number?: string; // Держ.№ PC
  route_number: number; // Номер маршрута
  shift?: string; // Смена
  driver_tab?: number; // Таб водителя
  driver_name?: string; // ФИО водителя
  conductor_tab?: number; // Таб кондуктора
  conductor_name?: string; // ФИО кондуктора
  departure_time?: string; // Время выхода
  arrival_time?: string; // Время захода
  route_endpoint?: string; // Конечная
  fuel_address?: string; // Адрес заправки
  status: string; // Статус
  notes?: string; // Примечания
}

export interface Route {
  id: number;
  number: number;
  name?: string;
  start_point?: string;
  end_point?: string;
  route_type?: string;
  distance?: number;
  travel_time?: number;
  first_departure?: string;
  last_departure?: string;
  interval_peak?: number;
  interval_normal?: number;
  depot?: string;
  fuel_address?: string;
  garage_address?: string;
  is_active: boolean;
  description?: string;
  notes?: string;
  display_name: string;
  route_info: string;
}

export interface Employee {
  id: number;
  tab_number: number;
  full_name: string;
  first_name?: string;
  last_name?: string;
  middle_name?: string;
  position?: string;
  category?: string;
  qualification?: string;
  hire_date?: string; // ISO date string
  department?: string;
  shift?: string;
  license_number?: string;
  license_category?: string;
  license_expiry?: string; // ISO date string
  phone?: string;
  email?: string;
  address?: string;
  is_active: boolean;
  notes?: string;
  display_name: string;
  short_name: string;
  is_driver: boolean;
  is_conductor: boolean;
}

export interface Vehicle {
  id: number;
  internal_number: string;
  state_number?: string;
  vehicle_type?: string;
  model?: string;
  manufacturer?: string;
  year?: number;
  capacity?: number;
  fuel_type?: string;
  engine_type?: string;
  route_number?: number;
  depot?: string;
  garage_number?: string;
  status: string;
  status_display: string;
  is_active: boolean;
  acquisition_date?: string; // ISO date string
  last_maintenance?: string; // ISO date string
  next_maintenance?: string; // ISO date string
  notes?: string;
  description?: string;
  display_name: string;
  full_name: string;
}

// API request/response types
export interface AssignmentFilters {
  skip?: number;
  limit?: number;
  route_number?: number;
  shift?: string;
  assignment_date?: string;
  driver_name?: string;
  status?: string;
  brigade?: string;
  application_number?: string;
  vehicle_number?: string;
}

export interface RouteFilters {
  skip?: number;
  limit?: number;
  route_type?: string;
  is_active?: boolean;
}

export interface EmployeeFilters {
  skip?: number;
  limit?: number;
  category?: string;
  is_active?: boolean;
  search?: string;
}

export interface VehicleFilters {
  skip?: number;
  limit?: number;
  vehicle_type?: string;
  route_number?: number;
  status?: string;
  is_active?: boolean;
}

export interface DispatcherStats {
  total_assignments: number;
  active_assignments: number;
  completed_assignments: number;
  total_routes: number;
  total_drivers: number;
  total_vehicles: number;
  shifts: {
    shift_1: number;
    shift_2: number;
    shift_3: number;
  };
  date: string; // ISO date string
}

// Table display types
export interface AssignmentTableColumn {
  key: keyof Assignment | keyof MSAccessAssignment;
  label: string;
  sortable?: boolean;
  width?: string;
  align?: "left" | "center" | "right";
  visible?: boolean;
}

export interface AssignmentTableRow extends Assignment {
  selected?: boolean;
}

export interface MSAccessTableRow extends MSAccessAssignment {
  selected?: boolean;
}

// Form types
export interface AssignmentFormData {
  route_number: number;
  shift?: string;
  assignment_date: string;
  brigade?: string;
  application_number?: string;
  address?: string;
  route_type?: string;
  internal_number?: string;
  fuel_route?: string;
  fuel_address?: string;
  driver_waybill?: string;
  driver_tab_number?: number;
  conductor_tab_number?: number;
  vehicle_number?: string;
  vehicle_model?: string;
  departure_time?: string;
  arrival_time?: string;
  hour1?: string;
  hour2?: string;
  hour3?: string;
  hour4?: string;
  hour5?: string;
  waybill_number?: string;
  departure_vzd?: string;
  departure_zgd?: string;
  end_kb?: string;
  break_1?: string;
  break_2?: string;
  profit_start?: string;
  profit_end?: string;
  route_endpoint?: string;
  notes?: string;
}

// API response types
export interface APIResponse<T> {
  data: T;
  message?: string;
  error?: boolean;
}

export interface APIError {
  error: boolean;
  message: string;
  details?: Array<{
    field: string;
    message: string;
    type: string;
  }>;
  status_code: number;
}

// API Response types for assignments
export interface AssignmentsResponse {
  assignments: Assignment[];
  total_count: number;
  date: string;
  statistics?: {
    total_assignments: number;
    active_assignments: number;
    total_routes: number;
    completed_assignments: number;
  };
}

export interface MSAccessAssignmentsResponse {
  assignments: MSAccessAssignment[];
  total_count: number;
  date: string;
  table_name: string;
  fields_count: number;
}

export interface StatisticsResponse {
  date: string;
  statistics: {
    total_assignments: number;
    active_assignments: number;
    total_routes: number;
    total_drivers: number;
    total_vehicles: number;
    shift_1_count: number;
    shift_2_count: number;
    shift_3_count: number;
  };
  summary: DispatcherStats;
}

// Shift types
export type ShiftType = "1" | "2" | "3";

export interface ShiftOption {
  value: ShiftType;
  label: string;
}

// Status types
export type AssignmentStatus = "active" | "completed" | "cancelled";
export type VehicleStatus =
  | "active"
  | "repair"
  | "maintenance"
  | "decommissioned"
  | "reserve";

// View types for dispatcher
export type DispatcherViewType = "simple" | "extended" | "full";

export interface DispatcherViewOption {
  value: DispatcherViewType;
  label: string;
  description: string;
}

// Column presets for different views
export const SIMPLE_COLUMNS: AssignmentTableColumn[] = [
  { key: "route_number", label: "Маршрут", sortable: true, width: "80px" },
  { key: "shift", label: "Смена", sortable: true, width: "70px" },
  { key: "driver_name", label: "Водитель", sortable: true, width: "200px" },
  { key: "vehicle_number", label: "Авто", sortable: true, width: "100px" },
  { key: "departure_time", label: "Выход", sortable: true, width: "80px" },
  { key: "arrival_time", label: "Заход", sortable: true, width: "80px" },
  { key: "status", label: "Статус", sortable: true, width: "100px" },
];

export const EXTENDED_COLUMNS: AssignmentTableColumn[] = [
  { key: "route_number", label: "Маршрут", sortable: true, width: "70px" },
  { key: "brigade", label: "Бр", sortable: true, width: "50px" },
  { key: "shift", label: "Смена", sortable: true, width: "60px" },
  { key: "driver_tab_number", label: "Таб", sortable: true, width: "60px" },
  { key: "driver_name", label: "Водитель", sortable: true, width: "180px" },
  { key: "conductor_name", label: "Кондуктор", sortable: true, width: "180px" },
  { key: "vehicle_number", label: "Авто", sortable: true, width: "80px" },
  { key: "state_number_pc", label: "Гос.№", sortable: true, width: "100px" },
  { key: "departure_time", label: "Выход", sortable: true, width: "70px" },
  { key: "arrival_time", label: "Заход", sortable: true, width: "70px" },
  { key: "waybill_number", label: "П.Л.", sortable: true, width: "80px" },
  { key: "fuel_address", label: "Заправка", sortable: true, width: "120px" },
  { key: "route_endpoint", label: "Конечная", sortable: true, width: "120px" },
  { key: "status", label: "Статус", sortable: true, width: "90px" },
];

export const FULL_MS_ACCESS_COLUMNS: AssignmentTableColumn[] = [
  {
    key: "date_charging",
    label: "Дата зарядки",
    sortable: true,
    width: "100px",
  },
  { key: "month", label: "Мт", sortable: true, width: "40px" },
  { key: "brigade", label: "Бр", sortable: true, width: "40px" },
  { key: "application", label: "Заявка", sortable: true, width: "80px" },
  { key: "address", label: "Адрес", sortable: true, width: "120px" },
  { key: "type", label: "Тип", sortable: true, width: "60px" },
  { key: "number_in", label: "№ в", sortable: true, width: "50px" },
  { key: "fuel_route", label: "Марш топливо", sortable: true, width: "100px" },
  { key: "driver_pb", label: "ПБ вод", sortable: true, width: "80px" },
  { key: "hour1", label: "Час1", sortable: true, width: "60px" },
  { key: "hour2", label: "Час2", sortable: true, width: "60px" },
  { key: "hour3", label: "Час3", sortable: true, width: "60px" },
  { key: "hour4", label: "Час4", sortable: true, width: "60px" },
  { key: "hour5", label: "Час5", sortable: true, width: "60px" },
  { key: "pb", label: "П.Б.", sortable: true, width: "60px" },
  { key: "vzd", label: "Взд", sortable: true, width: "60px" },
  { key: "zgd", label: "Згд", sortable: true, width: "60px" },
  { key: "kb", label: "К.Б.", sortable: true, width: "60px" },
  { key: "break_1", label: "Пер.1", sortable: true, width: "60px" },
  { key: "break_2", label: "Пер.2", sortable: true, width: "60px" },
  { key: "profit_start", label: "П.выг", sortable: true, width: "60px" },
  { key: "profit_end", label: "К.выг", sortable: true, width: "60px" },
  { key: "vehicle_number", label: "Н.авт", sortable: true, width: "60px" },
  { key: "vehicle_model", label: "М.авт", sortable: true, width: "100px" },
  { key: "vehicle_bedt", label: "М.Бедт", sortable: true, width: "80px" },
  { key: "coal", label: "Вугл", sortable: true, width: "60px" },
  { key: "vehicle_type", label: "Тип PC", sortable: true, width: "80px" },
  { key: "state_number", label: "Держ.№ PC", sortable: true, width: "100px" },
  { key: "route_number", label: "Маршрут", sortable: true, width: "80px" },
  { key: "shift", label: "Смена", sortable: true, width: "60px" },
  { key: "driver_name", label: "Водитель", sortable: true, width: "200px" },
  { key: "conductor_name", label: "Кондуктор", sortable: true, width: "200px" },
  { key: "departure_time", label: "Выход", sortable: true, width: "70px" },
  { key: "arrival_time", label: "Заход", sortable: true, width: "70px" },
  { key: "route_endpoint", label: "Конечная", sortable: true, width: "120px" },
  { key: "fuel_address", label: "Заправка", sortable: true, width: "120px" },
  { key: "status", label: "Статус", sortable: true, width: "90px" },
  { key: "notes", label: "Примечания", sortable: true, width: "150px" },
];
