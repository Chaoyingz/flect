import { cn } from "@/lib/utils";
import ReactMarkdown, { Components } from "react-markdown";
import remarkGfm from "remark-gfm";
import { CodeBlock } from "@/components/code-block";

export interface MarkdownProps {
  package: "docs-ui";
  type: "markdown";
  subType: "markdown";
  className?: string;
  text: string;
}

export function Markdown(props: MarkdownProps) {
  const { text, className } = props;
  const components: Components = {
    code({ children, className }) {
      const language = /language-(\w+)/.exec(className || "");
      if (!language) {
        return <code className={className}>{children}</code>;
      }
      return (
        <CodeBlock
          package="docs-ui"
          type="code-block"
          subType="code-block"
          text={children as string}
          language={language?.[1]}
        />
      );
    },
  };

  return (
    <ReactMarkdown
      className={cn(
        "prose prose-pre:bg-transparent prose-pre:p-0 max-w-screen-lg",
        className,
      )}
      remarkPlugins={[remarkGfm]}
      components={components}
    >
      {text}
    </ReactMarkdown>
  );
}
