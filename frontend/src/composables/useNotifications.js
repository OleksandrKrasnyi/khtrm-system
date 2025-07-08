import { useToast } from "vue-toastification";

export function useNotifications() {
  const toast = useToast();

  const showSuccess = (message, options = {}) => {
    toast.success(message, {
      timeout: 3000,
      closeOnClick: true,
      pauseOnFocusLoss: true,
      pauseOnHover: true,
      draggable: true,
      draggablePercent: 0.6,
      ...options,
    });
  };

  const showError = (message, options = {}) => {
    toast.error(message, {
      timeout: 5000,
      closeOnClick: true,
      pauseOnFocusLoss: true,
      pauseOnHover: true,
      draggable: true,
      draggablePercent: 0.6,
      ...options,
    });
  };

  const showWarning = (message, options = {}) => {
    toast.warning(message, {
      timeout: 4000,
      closeOnClick: true,
      pauseOnFocusLoss: true,
      pauseOnHover: true,
      draggable: true,
      draggablePercent: 0.6,
      ...options,
    });
  };

  const showInfo = (message, options = {}) => {
    toast.info(message, {
      timeout: 3000,
      closeOnClick: true,
      pauseOnFocusLoss: true,
      pauseOnHover: true,
      draggable: true,
      draggablePercent: 0.6,
      ...options,
    });
  };

  const showNotification = (type, message, options = {}) => {
    switch (type) {
      case "success":
        return showSuccess(message, options);
      case "error":
        return showError(message, options);
      case "warning":
        return showWarning(message, options);
      case "info":
        return showInfo(message, options);
      default:
        return showInfo(message, options);
    }
  };

  return {
    showSuccess,
    showError,
    showWarning,
    showInfo,
    showNotification,
  };
}
