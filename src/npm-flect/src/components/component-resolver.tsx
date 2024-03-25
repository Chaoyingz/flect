import { AnyComponentProps } from "@/types";

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
import { ComponentResolver } from "@/contexts/component-resolver";
import { Dialog } from "@/components/flect/dialog";
import { Display } from "@/components/flect/display";
import { DataGrid } from "@/components/flect/data-grid";
import { DeferredFetch } from "@/components/flect/deferred-fetch";

export const FlectComponentResolver: ComponentResolver = (
  props: AnyComponentProps,
) => {
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
    case "data-grid":
      return <DataGrid {...props} />;
    case "deferred-fetch":
      return <DeferredFetch {...props} />;
    case "dialog":
      return <Dialog {...props} />;
    case "display":
      return <Display {...props} />;
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
    default:
      return null;
  }
};
FlectComponentResolver.package = "flect";
