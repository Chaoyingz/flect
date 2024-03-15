import React, { createContext, useEffect, useState, ReactNode } from "react";
import { ComponentProps } from "@/types";

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

interface ComponentResolver {
  (props: ComponentProps): JSX.Element | null;
  package?: string;
}

interface ComponentResolverContextState {
  resolvers: { [resolverName: string]: ComponentResolver };
  registerResolver: (resolver: ComponentResolver) => void;
}

export const ComponentResolverContext = createContext<
  ComponentResolverContextState | undefined
>(undefined);

export const ComponentResolverProvider: React.FC<{
  children: ReactNode;
  resolver: ComponentResolver;
}> = ({ children, resolver }) => {
  const [resolvers, setResolvers] = useState<{
    [resolverName: string]: ComponentResolver;
  }>({});

  const registerResolver = (resolver: ComponentResolver) => {
    const resolverName = resolver.package;
    if (!resolverName) {
      console.warn(
        "Resolver function is anonymous and cannot be registered. Please provide a named function.",
      );
      return;
    }
    setResolvers((prevResolvers) => ({
      ...prevResolvers,
      [resolverName]: resolver,
    }));
  };

  useEffect(() => {
    registerResolver(resolver);
  }, [resolver]);

  return (
    <ComponentResolverContext.Provider value={{ resolvers, registerResolver }}>
      {children}
    </ComponentResolverContext.Provider>
  );
};

export const FlectComponentResolver: ComponentResolver = (
  props: ComponentProps,
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
