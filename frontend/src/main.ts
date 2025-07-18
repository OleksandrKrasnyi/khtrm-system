import { createApp } from "vue";
import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw,
} from "vue-router";
import { createPinia } from "pinia";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

import App from "./App.vue";
import "./style.css";
import type { Permission } from "@/types";

// Типы для meta информации маршрутов
interface CustomRouteMeta {
  requiresAuth?: boolean;
  requiresGuest?: boolean;
  requiresPermission?: Permission;
}

// Расширяем RouteRecordRaw для добавления типизации meta
declare module "vue-router" {
  interface RouteMeta extends CustomRouteMeta {}
}

// Create router
const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "home",
    redirect: () => {
      // Will be handled by navigation guard
      return "/dashboard";
    },
  },
  {
    path: "/login",
    name: "login",
    component: () => import("./components/LoginForm.vue"),
    meta: { requiresGuest: true },
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("./components/Dashboard.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/profile",
    name: "profile",
    component: () => import("./components/UserProfile.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/users",
    name: "users",
    component: () => import("./components/UserManagement.vue"),
    meta: { requiresAuth: true, requiresPermission: "can_manage_users" },
  },
  {
    path: "/vehicles",
    name: "vehicles",
    component: () => import("./components/VehicleManagement.vue"),
    meta: { requiresAuth: true, requiresPermission: "can_manage_vehicles" },
  },
  {
    path: "/assignments",
    name: "assignments",
    component: () => import("./components/AssignmentManagement.vue"),
    meta: { requiresAuth: true, requiresPermission: "can_create_assignments" },
  },
  {
    path: "/incidents",
    name: "incidents",
    component: () => import("./components/IncidentManagement.vue"),
    meta: { requiresAuth: true, requiresPermission: "can_record_incidents" },
  },
  {
    path: "/parking",
    name: "parking",
    component: () => import("./components/ParkingManagement.vue"),
    meta: { requiresAuth: true, requiresPermission: "can_manage_parking" },
  },
  {
    path: "/fuel",
    name: "fuel",
    component: () => import("./components/FuelManagement.vue"),
    meta: { requiresAuth: true, requiresPermission: "can_manage_fuel" },
  },
  {
    path: "/reports",
    name: "reports",
    component: () => import("./components/ReportsView.vue"),
    meta: { requiresAuth: true, requiresPermission: "can_view_reports" },
  },
  {
    path: "/settings",
    name: "settings",
    component: () => import("./components/SystemSettings.vue"),
    meta: { requiresAuth: true, requiresPermission: "can_manage_system" },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("./components/NotFound.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

// Navigation guards
router.beforeEach(async (to, from, next) => {
  // Import auth composable dynamically to avoid circular dependency
  const { useAuth } = await import("./composables/useAuth");
  const { isAuthenticated, checkPermission } = useAuth();

  // Check if route requires authentication
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next("/login");
    return;
  }

  // Check if route requires guest (unauthenticated) user
  if (to.meta.requiresGuest && isAuthenticated.value) {
    next("/dashboard");
    return;
  }

  // Check if route requires specific permission
  if (to.meta.requiresPermission && isAuthenticated.value) {
    if (!checkPermission(to.meta.requiresPermission)) {
      // Redirect to dashboard if user doesn't have permission
      next("/dashboard");
      return;
    }
  }

  next();
});

// Create Vue app
const app = createApp(App);

// Use plugins
app.use(createPinia());
app.use(router);
app.use(Toast, {
  position: "top-right",
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: "button",
  icon: true,
  rtl: false,
  toastClassName: "custom-toast",
  bodyClassName: "custom-toast-body",
  maxToasts: 5,
  newestOnTop: true,
});

// Global error handler
app.config.errorHandler = (error, instance, errorInfo) => {
  console.error("Global error:", error);
  console.error("Error info:", errorInfo);

  // Show user-friendly error message
  import("./composables/useNotifications").then(({ useNotifications }) => {
    const { showError } = useNotifications();
    showError("Виникла несподівана помилка. Спробуйте пізніше.");
  });
};

// Global properties
app.config.globalProperties.$appVersion = "1.0.0";

// Mount app
app.mount("#app");
