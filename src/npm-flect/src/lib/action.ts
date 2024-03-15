import { toast } from "sonner";

type Notify = {
  type: "notify";
  title: string;
  description?: string;
  position?:
    | "top-left"
    | "top-right"
    | "bottom-left"
    | "bottom-right"
    | "top-center"
    | "bottom-center";
  style?:
    | "normal"
    | "action"
    | "success"
    | "info"
    | "warning"
    | "error"
    | "loading"
    | "default";
};

type Redirect = {
  type: "redirect";
  url: string;
};

export type AnyAction = Notify | Redirect;

export type ActionResponse = {
  action: AnyAction;
};

export function executeAction(action: AnyAction) {
  switch (action.type) {
    case "notify": {
      const { title, style, ...rest } = action;
      switch (style) {
        case "success":
          toast.success(title, rest);
          break;
        case "info":
          toast.info(title, rest);
          break;
        case "warning":
          toast.warning(title, rest);
          break;
        case "error":
          toast.error(title, rest);
          break;
        default:
          toast(title, rest);
      }
      break;
    }
    case "redirect": {
      window.location.replace(action.url);
    }
  }
}
