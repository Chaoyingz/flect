import { useDispatchActionListen } from "@/hooks/use-dispatch-action-listen";
import { DispatchEventActionProps } from "@/lib/actions";
import { AnyComponentProps } from "@/types";
import { useState, useEffect } from "react";
import { AnyComponent } from "@/components/flect/any-component";

export interface DeferredFetchProps {
  package: "flect";
  type: "deferred-fetch";
  className?: string;
  path: string;
  trigger: DispatchEventActionProps;
}

export function DeferredFetch(props: DeferredFetchProps) {
  const { dispatched } = useDispatchActionListen(props.trigger.event);
  const [componentProps, setComponentProps] =
    useState<AnyComponentProps | null>(null);

  useEffect(() => {
    if (dispatched) {
      fetch(props.path)
        .then((response) => response.json())
        .then((json) => {
          console.log("body", json.body);
          setComponentProps(json.body);
        });
    }
  }, [dispatched, props.path]);

  useEffect(() => {
    console.log(componentProps);
  }, [componentProps]);

  return componentProps && <AnyComponent {...componentProps} />;
}
