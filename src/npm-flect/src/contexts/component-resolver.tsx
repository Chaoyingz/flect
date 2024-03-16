import React, { createContext, useEffect, useState, ReactNode } from "react";
import { AnyComponentProps } from "@/types";

export interface ComponentResolver {
  package: string;
  (props: AnyComponentProps): JSX.Element | null;
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
