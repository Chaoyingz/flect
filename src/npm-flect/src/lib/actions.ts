import { toast } from "sonner";
import { AnyActionProps } from "@/types";
import { ActionResolver } from "@/contexts/action-resolver";

export type NotifyAnyActionProps = {
  package: "flect";
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

export type RedirectAnyActionProps = {
  package: "flect";
  type: "redirect";
  url: string;
};

export function resolveAction(
  resolvers: { [resolverName: string]: ActionResolver },
  props: AnyActionProps | undefined,
) {
  if (!props) {
    return () => {};
  }

  const resolver = resolvers[props.package];
  if (!resolver) {
    throw new Error(
      `useAction: No action resolver found for package ${props.package}.`,
    );
  }

  const resolvedAction = resolver(props);
  if (resolvedAction === null) {
    throw new Error(
      `useAction: Action of type ${props.type} could not be resolved.`,
    );
  }

  return resolvedAction;
}

export function notifyAction(props: NotifyAnyActionProps) {
  const { title, style, ...rest } = props;
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
}

export function redirectAction(props: RedirectAnyActionProps) {
  window.location.replace(props.url);
}
