import { ActionResolver } from "@/contexts/action-resolver";
import {
  dispatchEventAction,
  notifyAction,
  redirectAction,
} from "@/lib/actions";
import { AnyActionProps } from "@/types";

export const FlectActionResolver: ActionResolver = (props: AnyActionProps) => {
  switch (props.type) {
    case "notify": {
      return () => notifyAction(props);
    }
    case "redirect": {
      return () => redirectAction(props);
    }
    case "dispatch-event": {
      return () => dispatchEventAction(props);
    }
  }

  return null;
};
FlectActionResolver.package = "flect";
