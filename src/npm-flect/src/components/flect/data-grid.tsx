import {
  useForm,
  FieldValues,
  useFieldArray,
  ControllerRenderProps,
} from "react-hook-form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Form as FormUI,
  FormControl,
  FormField,
  FormItem,
} from "@/components/ui/form";
import { ajvResolver } from "@/lib/ajv-resolver";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";
import { useContext } from "react";
import { Plus, RotateCw, Trash } from "lucide-react";
import { ActionResponse, Json } from "@/types";
import { resolveAction } from "@/lib/actions";
import { ActionResolverContext } from "@/contexts/action-resolver";
import { JSONSchema7 } from "json-schema";
import { getDefaultValues as getDefaultRowValues } from "@/lib/utils";
import React from "react";
import { FormTooltipMessage } from "./form";

interface InputAttrs {
  type: "text" | "password" | "email";
  placeholder?: string;
}

interface SelectAttrs {
  options: string[];
  placeholder?: string;
}

type Fieldtypes = "input" | "select";
type FieldAttrs = InputAttrs | SelectAttrs;

interface ModelRow extends JSONSchema7 {
  fieldType: Fieldtypes;
  editable: boolean;
  className?: string;
  attrs?: FieldAttrs;
  properties: {
    [key: string]: ModelRow;
  };
}

export interface Model extends JSONSchema7 {
  $defs: {
    [key: string]: ModelRow;
  };
  properties: {
    rows: {
      items: {
        $ref: string;
      };
    };
  };
}

export interface Dataset {
  [k: string]: Json;
}

export interface DataGridProps {
  package: "flect";
  type: "data-grid";
  className?: string;
  model: Model;
  datasets: Dataset[];
  submitUrl: string;
  submitText?: string;
}

function getDefinitionFromRef(schema: Model, ref: string) {
  const refParts = ref.match(/#\/\$defs\/(.+)/);
  if (!refParts) {
    throw new Error(`Invalid reference format: ${ref}`);
  }
  const definitionName = refParts[1];

  if (!schema.$defs || !schema.$defs[definitionName]) {
    throw new Error(`Definition not found for reference: ${ref}`);
  }
  return schema.$defs[definitionName];
}

function getRowSchema(schema: Model): ModelRow {
  return getDefinitionFromRef(schema, schema.properties.rows.items.$ref);
}

function getDefaultValues(datasets: Dataset[], defaultRowValues: FieldValues) {
  const rows = datasets.length > 0 ? datasets : [defaultRowValues];
  return { rows };
}

export function DataGrid(props: DataGridProps) {
  console.log(props);
  const { resolvers } = useContext(ActionResolverContext);
  const rowSchema = getRowSchema(props.model);
  const defaultRowValues = getDefaultRowValues(rowSchema);
  console.log("rowSchema", rowSchema);
  const form = useForm({
    resolver: ajvResolver(props.model, [
      "fieldType",
      "editable",
      "className",
      "attrs",
    ]),
    defaultValues: getDefaultValues(props.datasets, defaultRowValues),
  });
  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: "rows",
  });
  console.log(getDefaultValues(props.datasets, defaultRowValues));
  console.log(fields);
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
        className={cn(props.className)}
      >
        <Table>
          <div>
            <TableHeader>
              {Object.keys(rowSchema.properties).map((key, index) => {
                return (
                  <TableCell
                    key={index}
                    className={cn(
                      "px-3.5",
                      rowSchema.properties[key].className,
                    )}
                  >
                    {rowSchema.properties[key].title}
                  </TableCell>
                );
              })}
              <TableCell className="px-3.5">Actions</TableCell>
            </TableHeader>
          </div>
          <div>
            {fields.map((row, colIndex) => {
              return (
                <TableRow key={row.id} className="grid grid-cols-12">
                  {Object.keys(rowSchema.properties).map((key) => {
                    return (
                      <TableCell
                        key={`${row.id}-${key}`}
                        className={cn(
                          "p-0",
                          rowSchema.properties[key].className,
                        )}
                      >
                        <FormField
                          key={`${row.id}-${key}`}
                          control={form.control}
                          name={`rows.${colIndex}.${key}`}
                          render={({ field }) => (
                            <FormItem className="relative space-y-0">
                              <FormFieldSlot
                                schema={rowSchema.properties[key]}
                                control={field}
                              />
                              <FormTooltipMessage />
                            </FormItem>
                          )}
                        />
                      </TableCell>
                    );
                  })}
                  <TableCell className="invisible col-span-1 flex items-center px-2 group-hover:visible">
                    <Button
                      variant="ghost"
                      size={"sm"}
                      className="h-auto p-1.5"
                      onClick={() => remove(colIndex)}
                      type="button"
                    >
                      <Trash className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              );
            })}
          </div>
        </Table>
        <div className="text-destructive">
          {form.formState.errors.rows &&
            typeof form.formState.errors.rows.message === "string" && (
              <p>{form.formState.errors.rows.message}</p>
            )}
        </div>
        <div>
          <div className="border-b px-3.5">
            <button
              className="flex h-9 items-center gap-1 text-foreground/70 hover:text-foreground"
              onClick={() => append(defaultRowValues)}
              type="button"
            >
              <Plus className="h-4 w-4" />
              Add new field
            </button>
          </div>
        </div>
        <div className="mt-6">
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
        </div>
      </form>
    </FormUI>
  );
}

interface FormFieldSlotProps {
  schema: ModelRow;
  control: ControllerRenderProps<FieldValues, `rows.${number}.${string}`>;
}

function FormFieldSlot({ schema, control }: FormFieldSlotProps) {
  switch (schema.fieldType) {
    case "input":
      return (
        <FormControl>
          <Input
            className={cn(
              "focus:ring-none h-9 rounded-none border-0 bg-background ring-offset-0 focus:border focus:border-foreground focus:ring-0 focus-visible:ring-0 focus-visible:ring-offset-0 aria-invalid:border aria-invalid:border-destructive",
              schema.className,
            )}
            {...control}
            {...(schema.attrs as InputAttrs)}
            value={control.value ?? ""}
          />
        </FormControl>
      );
    case "select": {
      const attrs = schema.attrs as SelectAttrs;
      const options = schema.enum as string[];
      return (
        <Select
          onValueChange={control.onChange}
          defaultValue={control.value ?? ""}
          value={control.value ?? ""}
        >
          <FormControl>
            <SelectTrigger
              className={cn(
                "focus:ring-none z-10 h-9 rounded-none border-0 bg-background px-3.5 focus:border focus:ring-0 focus:ring-offset-0 focus-visible:ring-0 data-[state=open]:border data-[state=open]:border-foreground aria-invalid:border aria-invalid:border-destructive",
                schema.className,
              )}
            >
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
    default:
      return null;
  }
}

function Table({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return <div className={cn("border-t text-sm", className)}>{children}</div>;
}

function TableHeader({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "grid grid-cols-12 border-b font-medium text-primary",
        className,
      )}
    >
      {children}
    </div>
  );
}

function TableRow({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("group grid grid-cols-12 border-b", className)}>
      {children}
    </div>
  );
}

function TableCell({
  children,
  className,
}: {
  children?: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("h-9 border-r leading-9 last:border-0", className)}>
      {children}
    </div>
  );
}
