// Типы для пользователей
export interface User {
  id: number;
  username: string;
  email: string;
  role?: UserRole;
}

export interface UserRole {
  name: string;
  display_name_uk: string;
}

// Типы для аутентификации
export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  user: User;
  token: string;
}

// Типы для тестовых пользователей
export interface TestUser {
  username: string;
  password: string;
  role: UserRole;
  id: number;
}

// Типы для уведомлений
export interface NotificationOptions {
  timeout?: number;
  closeOnClick?: boolean;
  pauseOnFocusLoss?: boolean;
  pauseOnHover?: boolean;
  draggable?: boolean;
  draggablePercent?: number;
}

export type NotificationType = "success" | "error" | "warning" | "info";

// Типы для router
export interface RouteMetaAuthRequired {
  requiresAuth: true;
  requiresPermission?: string;
}

export interface RouteMetaGuestOnly {
  requiresGuest: true;
}

export interface RouteMetaOpen {
  requiresAuth?: false;
  requiresGuest?: false;
}

export type RouteMeta =
  | RouteMetaAuthRequired
  | RouteMetaGuestOnly
  | RouteMetaOpen;

// Типы для разрешений
export type Permission =
  | "can_manage_users"
  | "can_manage_vehicles"
  | "can_create_assignments"
  | "can_record_incidents"
  | "can_manage_parking"
  | "can_manage_fuel"
  | "can_view_reports"
  | "can_manage_system"
  | "can_manage_time";

export type RoleName =
  | "dispatcher"
  | "timekeeper_a"
  | "timekeeper_b"
  | "dispatcher_main"
  | "fuel_accountant"
  | "parking_manager"
  | "mechanic"
  | "driver"
  | "inspector"
  | "analyst"
  | "super_admin";

// Типы для API
export interface ApiResponse<T = Record<string, unknown>> {
  data: T;
  message?: string;
  success: boolean;
}

export interface ApiError {
  message: string;
  status: number;
}

// Типы для композаблов
export interface UseAuthReturn {
  isAuthenticated: Readonly<Ref<boolean>>;
  user: Readonly<Ref<User | null>>;
  userRole: Readonly<Ref<UserRole | null>>;
  login: (credentials: LoginCredentials) => Promise<boolean>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<boolean>;
  hasPermission: (permission: Permission) => boolean;
  checkPermission: (permission: Permission) => boolean;
}

export interface UseNotificationsReturn {
  showSuccess: (message: string, options?: NotificationOptions) => void;
  showError: (message: string, options?: NotificationOptions) => void;
  showWarning: (message: string, options?: NotificationOptions) => void;
  showInfo: (message: string, options?: NotificationOptions) => void;
  showNotification: (
    type: NotificationType,
    message: string,
    options?: NotificationOptions,
  ) => void;
  addNotification: (options: {
    type: NotificationType;
    message: string;
    [key: string]: unknown;
  }) => void;
}

// Импорты для внешних зависимостей
import type { Ref } from "vue";

// Экспорт интерфейсов для функциональности нарядчика
export * from "./dispatcher";
