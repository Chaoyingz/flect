import { type ClassValue, clsx } from "clsx";
import { JSONSchema7 } from "json-schema";
import { FieldValues } from "react-hook-form";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getMetaContent(name: string): string | undefined {
  return (
    document.querySelector(`meta[name="${name}"]`)?.getAttribute("content") ||
    undefined
  );
}

interface Model extends JSONSchema7 {
  properties: {
    [key: string]: Model;
  };
}

export function getDefaultValues(schema: Model) {
  const defaultRow: FieldValues = {};
  Object.keys(schema.properties).forEach((key) => {
    const prop = schema.properties[key];
    if (prop.default !== undefined && prop.default !== null) {
      defaultRow[key] = prop.default;
    } else {
      switch (prop.type) {
        case "string":
          defaultRow[key] = "";
          break;
        case "number":
        case "integer":
          defaultRow[key] = 0;
          break;
        case "boolean":
          defaultRow[key] = false;
          break;
        case "array":
          defaultRow[key] = [];
          break;
        case "object":
          defaultRow[key] = {};
          break;
        default:
          break;
      }
    }
  });
  return defaultRow;
}
