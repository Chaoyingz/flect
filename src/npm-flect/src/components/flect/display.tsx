import { Json } from "@/types";

export type DisplayType = "auto" | "boolean" | "json" | "null" | "text";

interface ValueProps {
  value: Json;
}

interface DisplayProps extends ValueProps {
  displayType: DisplayType;
}

export function Display({ displayType, value }: DisplayProps) {
  switch (displayType) {
    case "auto":
      return <AutoDisplay value={value} />;
    case "boolean":
      return <BooleanDisplay value={value} />;
    case "json":
      return <JsonDisplay value={value} />;
    case "null":
      return <NullDisplay />;
    case "text":
      return <TextDisplay value={value} />;
    default:
      return <AutoDisplay value={value} />;
  }
}

export function AutoDisplay({ value }: { value: Json }) {
  if (value === null) {
    return <NullDisplay />;
  } else if (typeof value === "boolean") {
    return <BooleanDisplay value={value} />;
  } else if (typeof value === "number") {
    return <>{value.toLocaleString()}</>;
  } else if (typeof value === "string") {
    return <TextDisplay value={value} />;
  } else {
    return <JsonDisplay value={value} />;
  }
}

export function BooleanDisplay({ value }: ValueProps) {
  return <>{value ? "true" : "false"}</>;
}

export function JsonDisplay({ value }: ValueProps) {
  return <pre>{JSON.stringify(value, null, 2)}</pre>;
}

export function NullDisplay() {
  return <>&#47;</>;
}

export function TextDisplay({ value }: ValueProps) {
  return <>{value}</>;
}
