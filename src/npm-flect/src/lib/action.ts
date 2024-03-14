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
  type:
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
      const { title, type } = action as Notify;
      switch (type) {
        case "success":
          toast.success(title, action);
          break;
        case "info":
          toast.info(title, action);
          break;
        case "warning":
          toast.warning(title, action);
          break;
        case "error":
          toast.error(title, action);
          break;
        default:
          toast(title, action);
      }
      break;
    }
    case "redirect": {
      const { url } = action as Redirect;
      window.location.replace(url);
    }
  }
}
