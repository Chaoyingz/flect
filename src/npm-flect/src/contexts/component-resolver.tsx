import React, {
  createContext,
  useEffect,
  useState,
  ReactNode,
  useContext,
} from "react";
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
  const context = useContext(ComponentResolverContext);
  const initialState = context
    ? { ...context.resolvers, [resolver.package]: resolver }
    : { [resolver.package]: resolver };

  const [resolvers, setResolvers] = useState<{
    [resolverName: string]: ComponentResolver;
  }>(initialState);

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
    console.log("resolver", resolver.package, resolver);
    console.log(resolvers);
  }, [resolver]);
  return (
    <ComponentResolverContext.Provider value={{ resolvers, registerResolver }}>
      {children}
    </ComponentResolverContext.Provider>
  );
};
