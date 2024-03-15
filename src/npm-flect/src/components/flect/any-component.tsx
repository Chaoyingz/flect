import { Avatar } from "@/components/flect/avatar";
import { Button } from "@/components/flect/button";
import { Container } from "@/components/flect/container";
import { Heading } from "@/components/flect/heading";
import { Link } from "@/components/flect/link";
import { Text } from "@/components/flect/text";
import { Table } from "@/components/flect/table";
import { Outlet } from "@/components/flect/outlet";
import { Form } from "@/components/flect/form";
import { NavLink } from "@/components/flect/nav-link";
import { Paragraph } from "@/components/flect/paragraph";
import { Markdown } from "@/components/flect/markdown";
import { CopyButton } from "@/components/flect/copy-button";
import { CodeBlock } from "@/components/flect/code-block";
import { Custom } from "@/components/flect/custom";
import { ComponentProps } from "@/types";

export function AnyComponent(props: ComponentProps): JSX.Element {
  switch (props.type) {
    case "avatar":
      return <Avatar {...props} />;
    case "button":
      return <Button {...props} />;
    case "code-block":
      return <CodeBlock {...props} />;
    case "container":
      return <Container {...props} />;
    case "copy-button":
      return <CopyButton {...props} />;
    case "custom":
      return <Custom {...props} />;
    case "form":
      return <Form {...props} />;
    case "heading":
      return <Heading {...props} />;
    case "link":
      return <Link {...props} />;
    case "markdown":
      return <Markdown {...props} />;
    case "nav-link":
      return <NavLink {...props} />;
    case "outlet":
      return <Outlet {...props} />;
    case "paragraph":
      return <Paragraph {...props} />;
    case "table":
      return <Table {...props} />;
    case "text":
      return <Text {...props} />;
  }
}

export function AnyComponents({ children }: { children?: ComponentProps[] }) {
  return (
    <>
      {children &&
        children.map((props, index) => <AnyComponent key={index} {...props} />)}
    </>
  );
}
