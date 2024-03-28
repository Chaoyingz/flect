import {
  Dialog as DialogUI,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { AnyComponentProps } from "@/types";
import { AnyComponents } from "@/components/flect/any-component";
import { cn } from "@/lib/utils";
import { DispatchEventActionProps } from "@/lib/actions";
import { useDispatchActionListen } from "@/hooks/use-dispatch-action-listen";
import { useEffect, useState } from "react";

export interface DialogProps {
  package: "flect";
  type: "dialog";
  className?: string;
  title?: string;
  description?: string;
  children?: AnyComponentProps[];
  defaultOpen: boolean;
  trigger?: DispatchEventActionProps;
}

export function Dialog(props: DialogProps) {
  const { dispatched, setDispatched } = useDispatchActionListen(
    props.trigger?.event || "",
  );
  const [isOpen, setIsOpen] = useState(props.defaultOpen);

  function setOpen(open: boolean) {
    setIsOpen(open);
    setDispatched(open);
  }

  useEffect(() => {
    if (dispatched) {
      setIsOpen(dispatched);
    }
  }, [dispatched]);

  return (
    <DialogUI open={isOpen} onOpenChange={setOpen}>
      <DialogContent className={cn("sm:max-w-[425px]", props.className)}>
        {(props.title || props.description) && (
          <DialogHeader>
            {props.title && <DialogTitle>{props.title}</DialogTitle>}
            {props.description && (
              <DialogDescription>{props.description}</DialogDescription>
            )}
          </DialogHeader>
        )}
        <AnyComponents children={props.children} />
      </DialogContent>
    </DialogUI>
  );
}
