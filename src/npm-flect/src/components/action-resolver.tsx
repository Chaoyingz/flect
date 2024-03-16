import { ActionResolver } from "@/contexts/action-resolver";
import { notifyAction, redirectAction } from "@/lib/actions";
import { AnyActionProps } from "@/types";

export const FlectActionResolver: ActionResolver = (props: AnyActionProps) => {
  switch (props.type) {
    case "notify": {
      return () => notifyAction(props);
    }
    case "redirect": {
      return () => redirectAction(props);
    }
  }

  return null;
};
FlectActionResolver.package = "flect";
