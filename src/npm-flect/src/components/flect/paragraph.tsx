import { cn } from "@/lib/utils";
import { ReactNode } from "react";
import { Link as RemixLink } from "react-router-dom";
import { linkVariants } from "./link.types";

export interface ParagraphProps {
  package: "flect";
  type: "paragraph";
  className?: string;
  text: string;
}

export function Paragraph(props: ParagraphProps) {
  const { text, className } = props;
  const renderText = (): ReactNode[] => {
    const pattern = /\[(.*?)\]\((.*?)\)/g;
    let lastIndex = 0;
    let match: RegExpExecArray | null;
    const result: ReactNode[] = [];

    while ((match = pattern.exec(text)) !== null) {
      if (match.index > lastIndex) {
        result.push(text.substring(lastIndex, match.index));
      }

      result.push(
        <RemixLink
          key={match.index}
          to={match[2]}
          className={cn(linkVariants({ underline: "always" }))}
          target="_blank"
        >
          {match[1]}
        </RemixLink>,
      );

      lastIndex = pattern.lastIndex;
    }

    if (lastIndex < text.length) {
      result.push(text.substring(lastIndex));
    }

    return result;
  };
  return <p className={className}>{renderText()}</p>;
}
