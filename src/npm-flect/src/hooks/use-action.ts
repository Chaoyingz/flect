import { useCallback, useContext } from "react";
import { AnyActionProps } from "@/types";
import { resolveAction } from "@/lib/actions";
import { ActionResolverContext } from "@/contexts/action-resolver";

export function useAction(props: AnyActionProps | undefined) {
  const { resolvers } = useContext(ActionResolverContext);

  return useCallback(() => resolveAction(resolvers, props), [resolvers, props]);
}
