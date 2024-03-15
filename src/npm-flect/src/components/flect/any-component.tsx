import { ResolverContext } from "@/resolver";
import { ComponentProps } from "@/types";
import { useContext } from "react";

export function AnyComponent(props: ComponentProps): JSX.Element {
  const context = useContext(ResolverContext);
  if (!context) {
    return (
      <p className="bg-destructive text-destructive-foreground">
        Component resolver context not found.
      </p>
    );
  }

  const { resolvers } = context;
  const resolver = resolvers[props.package];
  if (resolver) {
    const resolvedComponent = resolver(props);
    if (resolvedComponent === null) {
      return (
        <p className="bg-destructive text-destructive-foreground">
          Component of type {props.type} could not be resolved.
        </p>
      );
    }
    return resolvedComponent;
  }

  return (
    <p className="bg-destructive text-destructive-foreground">
      No component resolver found for type {props.type}.
    </p>
  );
}

export function AnyComponents({ children }: { children?: ComponentProps[] }) {
  return (
    <>
      {children &&
        children.map((props, index) => <AnyComponent key={index} {...props} />)}
    </>
  );
}
