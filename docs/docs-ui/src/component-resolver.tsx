import { ComponentResolver } from "@chaoying/flect";
import { Markdown, MarkdownProps } from "@/components/markdown.tsx";

type AnyComponentProps = MarkdownProps;

export const DocsUIComponentResolver: ComponentResolver = (
  props: AnyComponentProps,
) => {
  switch (props.subType) {
    case "markdown":
      return <Markdown {...props} />;
    default:
      return null;
  }
};
DocsUIComponentResolver.package = "docs-ui";
