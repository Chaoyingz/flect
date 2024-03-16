import { AnyActionProps } from "@/types";
import { ReactNode, createContext, useEffect, useState } from "react";

export interface ActionResolver {
  package: string;
  (props: AnyActionProps): (() => void) | null;
}

export interface ActionResolverContextState {
  resolvers: { [resolverName: string]: ActionResolver };
  registerResolver: (resolver: ActionResolver) => void;
}

const defaultContextValue: ActionResolverContextState = {
  resolvers: {},
  registerResolver: () => {},
};

export const ActionResolverContext =
  createContext<ActionResolverContextState>(defaultContextValue);

export const ActionResolverProvider: React.FC<{
  children: ReactNode;
  resolver: ActionResolver;
}> = ({ children, resolver }) => {
  const [resolvers, setResolvers] = useState<{
    [resolverName: string]: ActionResolver;
  }>({});

  const registerResolver = (resolver: ActionResolver) => {
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
    <ActionResolverContext.Provider value={{ resolvers, registerResolver }}>
      {children}
    </ActionResolverContext.Provider>
  );
};
