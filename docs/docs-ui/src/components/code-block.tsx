import { PrismLight as SyntaxHighlighter } from "react-syntax-highlighter";
import python from "react-syntax-highlighter/dist/esm/languages/prism/python";
import tsx from "react-syntax-highlighter/dist/esm/languages/prism/tsx";
import dracula from "react-syntax-highlighter/dist/esm/styles/prism/dracula";
import { CopyButton } from "@chaoying/flect/components";

import { cn } from "@/lib/utils";

SyntaxHighlighter.registerLanguage("python", python);
SyntaxHighlighter.registerLanguage("tsx", tsx);

export type CodeBlockProps = {
  package: "docs-ui";
  type: "code-block";
  subType: "code-block";
  className?: string;
  text: string;
  language?: string;
};

export function CodeBlock(props: CodeBlockProps) {
  return (
    <div className="relative">
      <CopyButton
        package="flect"
        type="copy-button"
        value={props.text}
        className="absolute right-4 top-3 z-20 h-6 w-6 p-1.5"
      />
      <SyntaxHighlighter
        className={cn(props.className)}
        PreTag="div"
        language={props.language}
        style={dracula}
        wrapLongLines
      >
        {props.text}
      </SyntaxHighlighter>
    </div>
  );
}
