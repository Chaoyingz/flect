import { cn } from "@/lib/utils";

export interface HeadingProps {
  package: "flect";
  type: "heading";
  className?: string;
  level: 1 | 2 | 3 | 4 | 5 | 6;
  text: string;
  id?: string;
}

export function Heading(props: HeadingProps) {
  const { level, text, id } = props;
  const Tag = `h${level}` as keyof JSX.IntrinsicElements;
  return (
    <Tag id={id} className={cn("font-semibold", props.className)}>
      {text}
    </Tag>
  );
}
