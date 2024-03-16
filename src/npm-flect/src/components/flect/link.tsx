import { cn } from "@/lib/utils";
import { AnyComponents } from "@/components/flect/any-component";
import { Link as RemixLink } from "react-router-dom";
import { VariantProps } from "class-variance-authority";
import { linkVariants } from "@/components/flect/link.types";
import { AnyComponentProps } from "@/types";

export interface LinkProps extends VariantProps<typeof linkVariants> {
  package: "flect";
  type: "link";
  className?: string;
  href: string;
  target?: "_self" | "_blank";
  children?: AnyComponentProps[];
}

export function Link(props: LinkProps) {
  const { href, underline, children, className } = props;
  return (
    <RemixLink
      to={href}
      className={cn(linkVariants({ underline, className }))}
      target={props.target}
    >
      <AnyComponents children={children} />
    </RemixLink>
  );
}
