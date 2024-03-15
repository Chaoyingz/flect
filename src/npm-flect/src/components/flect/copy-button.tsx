import {
  Button as ButtonUI,
  ButtonProps as ButtonPropsUI,
} from "@/components/ui/button";
import { cn } from "@/lib/utils";
import React from "react";
import { Check, Copy } from "lucide-react";

export interface CopyButtonProps extends Omit<ButtonPropsUI, "type"> {
  package: "flect";
  type: "copy-button";
  className?: string;
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export function CopyButton({ type, ...props }: CopyButtonProps) {
  const [isCopied, setIsCopied] = React.useState(false);

  return (
    <ButtonUI
      size="sm"
      className={cn("h-6 w-6 px-0", props.className)}
      onClick={() => {
        if (typeof window === "undefined") return;
        setIsCopied(true);
        void window.navigator.clipboard.writeText(
          props.value?.toString() ?? "",
        );
        setTimeout(() => setIsCopied(false), 2000);
      }}
      {...props}
    >
      {isCopied ? (
        <Check className="h-4 w-4" aria-hidden="true" />
      ) : (
        <Copy className="h-4 w-4" aria-hidden="true" />
      )}
      <span className="sr-only">
        {isCopied ? "Copied" : "Copy to clipboard"}
      </span>
    </ButtonUI>
  );
}
