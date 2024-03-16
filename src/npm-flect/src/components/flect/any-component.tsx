import { ComponentResolverContext } from "@/contexts/component-resolver";
import { AnyComponentProps } from "@/types";
import { useContext } from "react";

export function AnyComponent(props: AnyComponentProps): JSX.Element {
  const context = useContext(ComponentResolverContext);
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

export function AnyComponents({
  children,
}: {
  children?: AnyComponentProps[];
}) {
  return (
    <>
      {children &&
        children.map((props, index) => <AnyComponent key={index} {...props} />)}
    </>
  );
}
