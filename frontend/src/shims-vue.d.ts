declare module "*.vue" {
  import type { DefineComponent } from "vue";
  const component: DefineComponent<
    Record<string, unknown>,
    Record<string, unknown>,
    Record<string, unknown>
  >;
  export default component;
}

declare module "vue-toastification" {
  import { App } from "vue";

  export interface ToastOptions {
    timeout?: number;
    closeOnClick?: boolean;
    pauseOnFocusLoss?: boolean;
    pauseOnHover?: boolean;
    draggable?: boolean;
    draggablePercent?: number;
    showCloseButtonOnHover?: boolean;
    hideProgressBar?: boolean;
    closeButton?: string;
    icon?: boolean;
    rtl?: boolean;
    toastClassName?: string;
    bodyClassName?: string;
    maxToasts?: number;
    newestOnTop?: boolean;
    position?: string;
  }

  export interface ToastInterface {
    success: (message: string, options?: ToastOptions) => void;
    error: (message: string, options?: ToastOptions) => void;
    warning: (message: string, options?: ToastOptions) => void;
    info: (message: string, options?: ToastOptions) => void;
  }

  export function useToast(): ToastInterface;

  const plugin: {
    install: (app: App, options?: ToastOptions) => void;
  };

  export default plugin;
}
