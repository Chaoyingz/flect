export interface CustomProps {
  package: "flect";
  type: "custom";
  className?: string;
  subType: string;
}

export function Custom(props: CustomProps) {
  return (
    <p className="bg-destructive text-destructive-foreground">
      The custom component <code>{props.subType}</code> component is not
      implemented yet.
    </p>
  );
}
