import { cn } from "@/lib/utils.ts";

export interface BadgeProps {
  package: "docs-ui";
  type: "badge";
  subType: "badge";
  className?: string;
  text: string;
}

export const Badge = (props: BadgeProps) => {
  return (
    <div
      className={cn(
        "inline-flex rounded-md bg-primary px-2.5 py-1 text-xs font-semibold text-primary-foreground",
        props.className,
      )}
    >
      {props.text}
    </div>
  );
};
