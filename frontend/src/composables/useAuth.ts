import { ref, computed, type Ref } from "vue";
import type {
  User,
  UserRole,
  LoginCredentials,
  TestUser,
  Permission,
  RoleName,
  UseAuthReturn,
} from "@/types";

// Global authentication state
const currentUser: Ref<User | null> = ref(null);
const currentUserRole: Ref<UserRole | null> = ref(null);
const authToken: Ref<string | null> = ref(localStorage.getItem("auth_token"));

// Restore state from localStorage on initialization
if (authToken.value) {
  // Try to restore user data from token
  const userId = authToken.value.replace("token-", "");
  const testUsers: Record<string, TestUser> = {
    "0": {
      username: "admin",
      password: "admin",
      role: { name: "super_admin", display_name_uk: "Адміністратор" },
      id: 0,
    },
    "1": {
      username: "nar",
      password: "nar",
      role: { name: "dispatcher", display_name_uk: "Нарядчик" },
      id: 1,
    },
    "2": {
      username: "taba",
      password: "taba",
      role: { name: "timekeeper_a", display_name_uk: "Табельник A" },
      id: 2,
    },
    "3": {
      username: "tabb",
      password: "tabb",
      role: { name: "timekeeper_b", display_name_uk: "Табельник B" },
      id: 3,
    },
    "4": {
      username: "dys",
      password: "dys",
      role: { name: "dispatcher_main", display_name_uk: "Диспетчер" },
      id: 4,
    },
    "5": {
      username: "buc",
      password: "buc",
      role: { name: "fuel_accountant", display_name_uk: "Бухгалтер з палива" },
      id: 5,
    },
  };

  const userData = testUsers[userId];
  if (userData) {
    currentUser.value = {
      id: userData.id,
      username: userData.username,
      email: `${userData.username}@khtrm.kharkiv.ua`,
      role: userData.role,
    };
    currentUserRole.value = userData.role;
  }
}

export function useAuth(): UseAuthReturn {
  // Computed properties
  const isAuthenticated = computed(() => !!authToken.value);
  const user = computed(() => currentUser.value);
  const userRole = computed(() => currentUserRole.value);

  // Predefined test users
  const testUsers: Record<string, TestUser> = {
    admin: {
      username: "admin",
      password: "admin",
      role: { name: "super_admin", display_name_uk: "Адміністратор" },
      id: 0,
    },
    nar: {
      username: "nar",
      password: "nar",
      role: { name: "dispatcher", display_name_uk: "Нарядчик" },
      id: 1,
    },
    taba: {
      username: "taba",
      password: "taba",
      role: { name: "timekeeper_a", display_name_uk: "Табельник A" },
      id: 2,
    },
    tabb: {
      username: "tabb",
      password: "tabb",
      role: { name: "timekeeper_b", display_name_uk: "Табельник B" },
      id: 3,
    },
    dys: {
      username: "dys",
      password: "dys",
      role: { name: "dispatcher_main", display_name_uk: "Диспетчер" },
      id: 4,
    },
    buc: {
      username: "buc",
      password: "buc",
      role: { name: "fuel_accountant", display_name_uk: "Бухгалтер з палива" },
      id: 5,
    },
  };

  // Methods
  const login = async (credentials: LoginCredentials): Promise<boolean> => {
    try {
      // Check if user exists and password matches
      const user = testUsers[credentials.username];
      if (!user || user.password !== credentials.password) {
        throw new Error("Invalid credentials");
      }

      // Set authentication state
      authToken.value = `token-${user.id}`;
      currentUser.value = {
        id: user.id,
        username: user.username,
        email: `${user.username}@khtrm.kharkiv.ua`,
        role: user.role,
      };
      currentUserRole.value = user.role;

      localStorage.setItem("auth_token", authToken.value);
      return true;
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  };

  const logout = async (): Promise<void> => {
    try {
      // TODO: Call API for logout
      authToken.value = null;
      currentUser.value = null;
      currentUserRole.value = null;
      localStorage.removeItem("auth_token");
    } catch (error) {
      console.error("Logout error:", error);
      throw error;
    }
  };

  const checkAuth = async (): Promise<boolean> => {
    if (!authToken.value) return false;

    try {
      // TODO: Check token validity through API
      return true;
    } catch (error) {
      console.error("Auth check error:", error);
      await logout();
      return false;
    }
  };

  const hasPermission = (permission: Permission): boolean => {
    if (!currentUserRole.value) return false;

    // Супер-администратор имеет все права
    if (currentUserRole.value.name === "super_admin") return true;

    // Проверяем конкретные права на основе роли
    const rolePermissions: Record<RoleName, Permission[]> = {
      dispatcher: ["can_create_assignments", "can_view_reports"],
      timekeeper_a: ["can_manage_time", "can_view_reports"],
      timekeeper_b: ["can_manage_time", "can_view_reports"],
      dispatcher_main: ["can_create_assignments", "can_view_reports"],
      fuel_accountant: ["can_manage_fuel", "can_view_reports"],
      parking_manager: ["can_manage_parking", "can_view_reports"],
      mechanic: ["can_record_incidents"],
      driver: [],
      inspector: ["can_record_incidents", "can_view_reports"],
      analyst: ["can_view_reports"],
      super_admin: [
        "can_manage_users",
        "can_manage_vehicles",
        "can_create_assignments",
        "can_record_incidents",
        "can_manage_parking",
        "can_manage_fuel",
        "can_view_reports",
        "can_manage_system",
        "can_manage_time",
      ],
    };

    const roleName = currentUserRole.value.name as RoleName;
    const userPermissions = rolePermissions[roleName] || [];
    return userPermissions.includes(permission);
  };

  const checkPermission = hasPermission; // Alias для совместимости с router

  return {
    // State
    isAuthenticated,
    user,
    userRole,

    // Methods
    login,
    logout,
    checkAuth,
    hasPermission,
    checkPermission,
  };
}
