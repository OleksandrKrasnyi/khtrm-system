import { ref, computed } from "vue";

// Глобальное состояние аутентификации
const currentUser = ref(null);
const currentUserRole = ref(null);
const authToken = ref(localStorage.getItem("auth_token"));

export function useAuth() {
  // Computed properties
  const isAuthenticated = computed(() => !!authToken.value);
  const user = computed(() => currentUser.value);
  const userRole = computed(() => currentUserRole.value);

  // Predefined users for testing
  const testUsers = {
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
  const login = async (credentials) => {
    try {
      console.log("Login attempt:", credentials);

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
      };
      currentUserRole.value = user.role;

      localStorage.setItem("auth_token", authToken.value);
      return true;
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      // TODO: Вызов API для logout
      authToken.value = null;
      currentUser.value = null;
      currentUserRole.value = null;
      localStorage.removeItem("auth_token");
    } catch (error) {
      console.error("Logout error:", error);
      throw error;
    }
  };

  const checkAuth = async () => {
    if (!authToken.value) return false;

    try {
      // TODO: Проверка валидности токена через API
      console.log("Checking auth token validity");
      return true;
    } catch (error) {
      console.error("Auth check error:", error);
      await logout();
      return false;
    }
  };

  const hasPermission = (permission) => {
    if (!currentUserRole.value) return false;

    // Супер-администратор имеет все права
    if (currentUserRole.value.name === "super_admin") return true;

    // Проверяем конкретные права на основе роли
    const rolePermissions = {
      dispatcher: ["can_create_assignments", "can_view_reports"],
      timekeeper: ["can_manage_time", "can_view_reports"],
      parking_manager: ["can_manage_parking", "can_view_reports"],
      fuel_manager: ["can_manage_fuel", "can_view_reports"],
      mechanic: ["can_record_incidents"],
      driver: [],
      inspector: ["can_record_incidents", "can_view_reports"],
      analyst: ["can_view_reports"],
    };

    const userPermissions = rolePermissions[currentUserRole.value.name] || [];
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
