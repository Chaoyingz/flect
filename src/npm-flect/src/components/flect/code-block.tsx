import { CopyButton } from "@/components/flect/copy-button";
import { cn } from "@/lib/utils";

export type CodeBlockProps = {
  type: "code-block";
  className?: string;
  text: string;
  language?: string;
};

export function CodeBlock({ text, ...props }: CodeBlockProps) {
  return (
    <div
      className={cn(
        "relative max-h-[640px] overflow-x-auto rounded-lg border bg-zinc-950 p-4 py-4 font-mono text-sm text-muted-foreground",
        props.className,
      )}
    >
      <CopyButton
        value={text}
        className="absolute right-4 top-3 z-20 h-6 w-6 p-1.5"
        type="copy-button"
      />
      {text}
    </div>
  );
}
