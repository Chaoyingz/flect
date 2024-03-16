import { AnyComponents } from "@/components/flect/any-component";
import { AnyComponentProps } from "@/types";

export interface ContainerProps {
  package: "flect";
  type: "container";
  className?: string;
  children?: AnyComponentProps[];
  tag: "div" | "section" | "header" | "footer" | "main" | "nav" | "aside";
}

export function Container(props: ContainerProps) {
  const { children, className, tag } = props;
  const Tag = tag || "div";
  return (
    <Tag className={className}>
      <AnyComponents children={children} />
    </Tag>
  );
}
