import { useForm, FieldValues, ControllerRenderProps } from "react-hook-form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Form as FormUI,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { JSONSchema7 } from "json-schema";
import { Textarea } from "@/components/ui/textarea";
import { ajvResolver } from "@/lib/ajv-resolver";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";
import React from "react";
import { ActionResponse, executeAction } from "@/lib/action";
import { RotateCw } from "lucide-react";

interface InputAttrs {
  type: "text" | "password" | "email";
  placeholder?: string;
}

interface TextAreaAttrs {
  rows?: number;
  cols?: number;
  placeholder?: string;
}

interface SelectAttrs {
  options: string[];
}

type Fieldtypes = "checkbox" | "input" | "select" | "textarea";
type FieldAttrs = InputAttrs | TextAreaAttrs | SelectAttrs;

interface Model extends JSONSchema7 {
  fieldType: Fieldtypes;
  className?: string;
  attrs?: FieldAttrs;
  properties: {
    [key: string]: Model;
  };
}

export interface FormLazyProps {
  type: "form";
  className?: string;
  model: Model;
  submitUrl: string;
  submitText?: string;
}

function getDefaultValues(schema: Model): FieldValues {
  const defaults: FieldValues = {};
  Object.keys(schema.properties).forEach((key) => {
    const prop = schema.properties[key];
    if (prop.default !== undefined) {
      defaults[key] = prop.default;
    }
  });
  return defaults;
}

export default function FormLazy(props: FormLazyProps) {
  const form = useForm({
    resolver: ajvResolver(props.model),
    defaultValues: getDefaultValues(props.model),
  });
  async function onSubmit(values: FieldValues) {
    const response = await fetch(props.submitUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(values),
    });
    if (!response.ok) {
      throw new Error(response.statusText);
    }
    const action = (await response.json()) as ActionResponse;
    executeAction(action.action);
  }
  return (
    <FormUI {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className={cn("space-y-8", props.className)}
      >
        {props.model.properties &&
          Object.entries(props.model.properties).map(([key, value]) => {
            let modifiedAttrs = value.attrs;
            if (value.fieldType === "select" && value.enum) {
              modifiedAttrs = {
                ...value.attrs,
                options: value.enum as string[],
              };
            }
            if (
              typeof value === "object" &&
              value !== null &&
              !Array.isArray(value)
            ) {
              return (
                <FormField
                  key={key}
                  control={form.control}
                  name={key}
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>{value.title || key}</FormLabel>
                      <FormControl>
                        <FormFieldSlot
                          fieldType={value.fieldType}
                          attrs={modifiedAttrs}
                          field={field}
                          className={value.className}
                        />
                      </FormControl>
                      <FormDescription>{value.description}</FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              );
            }
            return null;
          })}
        {form.formState.isSubmitting ? (
          <Button
            type="submit"
            className="w-36"
            disabled={form.formState.isSubmitting}
          >
            <RotateCw className="mr-2 h-4 w-4 animate-spin" />
            Submitting...
          </Button>
        ) : (
          <Button type="submit" className="min-w-36">
            {props.submitText || "Submit"}
          </Button>
        )}
      </form>
    </FormUI>
  );
}

interface FormFieldSlotProps {
  fieldType: Fieldtypes;
  attrs?: FieldAttrs;
  className?: string;
  field: ControllerRenderProps;
}

const FormFieldSlot = React.memo(
  ({ fieldType, attrs, field, className }: FormFieldSlotProps) => {
    switch (fieldType) {
      case "checkbox":
        return <Checkbox className={className} {...field} />;
      case "input":
        return (
          <Input className={className} {...field} {...(attrs as InputAttrs)} />
        );
      case "select": {
        const { options } = attrs as SelectAttrs;
        return (
          <Select
            onValueChange={field.onChange}
            defaultValue={field.value}
            value={field.value}
          >
            <SelectTrigger className={cn("w-[180px]", className)}>
              <SelectValue placeholder={field.name} />
            </SelectTrigger>
            <SelectContent>
              {options.map((value) => (
                <SelectItem key={value} value={value}>
                  {value}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        );
      }
      case "textarea":
        return (
          <Textarea
            className={className}
            {...field}
            {...(attrs as TextAreaAttrs)}
          />
        );
      default:
        return null;
    }
  },
);
