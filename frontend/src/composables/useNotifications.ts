import { useToast } from "vue-toastification";
import type {
  NotificationOptions,
  NotificationType,
  UseNotificationsReturn,
} from "@/types";

export function useNotifications(): UseNotificationsReturn {
  const toast = useToast();

  const showSuccess = (
    message: string,
    options: NotificationOptions = {},
  ): void => {
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

  const showError = (
    message: string,
    options: NotificationOptions = {},
  ): void => {
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

  const showWarning = (
    message: string,
    options: NotificationOptions = {},
  ): void => {
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

  const showInfo = (
    message: string,
    options: NotificationOptions = {},
  ): void => {
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

  const showNotification = (
    type: NotificationType,
    message: string,
    options: NotificationOptions = {},
  ): void => {
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

  // Alternative function that accepts options object with type and message
  const addNotification = (options: {
    type: NotificationType;
    message: string;
    [key: string]: unknown;
  }) => {
    const { type, message, ...notificationOptions } = options;
    showNotification(type, message, notificationOptions as NotificationOptions);
  };

  return {
    showSuccess,
    showError,
    showWarning,
    showInfo,
    showNotification,
    addNotification,
  };
}
