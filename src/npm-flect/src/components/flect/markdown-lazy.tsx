import { cn } from "@/lib/utils";
import ReactMarkdown, { Components } from "react-markdown";
import remarkGfm from "remark-gfm";
import { CodeBlock } from "./code-block";

export interface MarkdownLazyProps {
  type: "markdown";
  className?: string;
  text: string;
}

export default function Markdown(props: MarkdownLazyProps) {
  const { text, className } = props;
  const components: Components = {
    code({ children, className }) {
      const language = /language-(\w+)/.exec(className || "");
      if (!language) {
        return <code className={className}>{children}</code>;
      }
      return (
        <CodeBlock
          text={children as string}
          type="code-block"
          language={language?.[1]}
        />
      );
    },
  };

  return (
    <ReactMarkdown
      className={cn("prose prose-pre:bg-transparent prose-pre:p-0", className)}
      remarkPlugins={[remarkGfm]}
      components={components}
    >
      {text}
    </ReactMarkdown>
  );
}
