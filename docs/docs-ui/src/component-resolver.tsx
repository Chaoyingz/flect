import { BadgeProps, Badge } from "@/components/badge";
import { ComponentResolver } from "@chaoying/flect";

type AnyComponentProps = BadgeProps;

export const DocsUIComponentResolver: ComponentResolver = (
  props: AnyComponentProps,
) => {
  switch (props.subType) {
    case "badge":
      return <Badge {...props} />;
    default:
      return null;
  }
};
DocsUIComponentResolver.package = "docs-ui";
