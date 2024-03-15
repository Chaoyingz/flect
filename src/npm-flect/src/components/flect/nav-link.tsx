import { cn } from "@/lib/utils";
import { AnyComponents } from "@/components/flect/any-component";
import { NavLink as RemixNavLink } from "react-router-dom";
import { LinkProps } from "@/components/flect/link";
import { linkVariants } from "@/components/flect/link.types";

export interface NavLinkProps extends Omit<LinkProps, "type"> {
  package: "flect";
  type: "nav-link";
}

export function NavLink(props: NavLinkProps) {
  const { href, underline, className, children } = props;
  return (
    <RemixNavLink
      to={href}
      className={({ isActive }) =>
        cn(linkVariants({ underline, isActive, className }))
      }
      target={props.target}
    >
      <AnyComponents children={children} />
    </RemixNavLink>
  );
}
