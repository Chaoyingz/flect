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
  useFormField,
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
import { cn, getDefaultValues } from "@/lib/utils";
import React, { useContext } from "react";
import { RotateCw, ShieldAlert } from "lucide-react";
import { ActionResponse } from "@/types";
import { resolveAction } from "@/lib/actions";
import { ActionResolverContext } from "@/contexts/action-resolver";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface CheckboxAttrs {
  checked?: boolean;
}

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
  placeholder?: string;
}

type Fieldtypes = "checkbox" | "input" | "select" | "textarea";
type FieldAttrs = CheckboxAttrs | InputAttrs | SelectAttrs | TextAreaAttrs;

interface Model extends JSONSchema7 {
  fieldType: Fieldtypes;
  className?: string;
  attrs?: FieldAttrs;
  properties: {
    [key: string]: Model;
  };
}

export interface FormProps {
  package: "flect";
  type: "form";
  className?: string;
  model: Model;
  submitUrl: string;
  submitText?: string;
}

export function Form(props: FormProps) {
  const { resolvers } = useContext(ActionResolverContext);
  const form = useForm({
    resolver: ajvResolver(props.model, ["fieldType", "className", "attrs"]),
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
    const responseJson = (await response.json()) as ActionResponse;
    resolveAction(resolvers, responseJson.action)();
  }

  return (
    <FormUI {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className={cn("space-y-8", props.className)}
      >
        {props.model.properties &&
          Object.entries(props.model.properties).map(([key, value]) => {
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
                      <FormFieldSlot schema={value} control={field} />
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
  schema: Model;
  control: ControllerRenderProps;
}

const FormFieldSlot = React.memo(({ schema, control }: FormFieldSlotProps) => {
  switch (schema.fieldType) {
    case "checkbox":
      return (
        <FormControl>
          <Checkbox
            className={schema.className}
            {...control}
            value={control.value ?? ""}
          />
        </FormControl>
      );
    case "input":
      return (
        <FormControl>
          <Input
            className={schema.className}
            {...control}
            {...(schema.attrs as InputAttrs)}
            value={control.value ?? ""}
          />
        </FormControl>
      );
    case "select": {
      const options = schema.enum as string[];
      const attrs = schema.attrs as SelectAttrs;
      return (
        <Select
          onValueChange={control.onChange}
          defaultValue={control.value}
          value={control.value ?? ""}
        >
          <FormControl>
            <SelectTrigger className={cn("w-[180px]", schema.className)}>
              <SelectValue
                placeholder={attrs.placeholder || `Select ${schema.title}`}
              />
            </SelectTrigger>
          </FormControl>
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
        <FormControl>
          <Textarea
            className={schema.className}
            {...control}
            {...(schema.attrs as TextAreaAttrs)}
            value={control.value ?? ""}
          />
        </FormControl>
      );
    default:
      return null;
  }
});

export const FormTooltipMessage = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
  // eslint-disable-next-line
>(({ className, children, ...props }, _) => {
  const { error, formMessageId } = useFormField();
  const body = error ? String(error?.message) : children;

  if (!body) {
    return null;
  }

  return (
    <Tooltip id={formMessageId} {...props}>
      <TooltipTrigger asChild>
        <div className="absolute right-2 top-0 z-10 flex h-full items-center justify-center">
          <ShieldAlert size="18" className="bg-background text-destructive" />
        </div>
      </TooltipTrigger>
      <TooltipContent
        className={cn("text-sm font-medium text-destructive", className)}
      >
        {body}
      </TooltipContent>
    </Tooltip>
  );
});
FormTooltipMessage.displayName = "FormTooltipMessage";
