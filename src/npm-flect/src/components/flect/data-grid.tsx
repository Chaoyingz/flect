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
import { RotateCw } from "lucide-react";
import { ActionResponse, Json } from "@/types";
import { resolveAction } from "@/lib/actions";
import { ActionResolverContext } from "@/contexts/action-resolver";
import { JSONSchema7 } from "json-schema";
import {
  Table,
  TableRow,
  TableCell,
  TableHead,
  TableHeader,
  TableBody,
} from "@/components/ui/table";
import { getDefaultValues as getDefaultRowValues } from "@/lib/utils";
import React from "react";

interface InputAttrs {
  type: "text" | "password" | "email";
  placeholder?: string;
}

interface SelectAttrs {
  options: string[];
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
  const { fields, append } = useFieldArray({
    control: form.control,
    name: "rows",
  });
  console.log(form.getValues());
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
        className={cn("space-y-8", props.className)}
      >
        <Table>
          <TableHeader>
            <TableRow>
              {Object.keys(rowSchema.properties).map((key, index) => {
                return (
                  <TableHead key={index}>
                    {rowSchema.properties[key].title}
                  </TableHead>
                );
              })}
            </TableRow>
          </TableHeader>
          <TableBody>
            {fields.map((row, colIndex) => {
              return (
                <TableRow key={row.id}>
                  {Object.keys(rowSchema.properties).map((key) => {
                    return (
                      <TableCell key={`${row.id}-${key}`}>
                        <FormField
                          control={form.control}
                          name={`rows.${colIndex}.${key}`}
                          render={({ field }) => (
                            <FormItem>
                              <FormControl>
                                <FormFieldSlot
                                  schema={rowSchema.properties[key]}
                                  control={field}
                                />
                              </FormControl>
                            </FormItem>
                          )}
                        />
                      </TableCell>
                    );
                  })}
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
        <div>
          <div className="border-b px-3.5">
            <button
              className="flex h-9 items-center gap-1 text-secondary-foreground hover:text-primary-foreground"
              onClick={() => append(defaultRowValues)}
              type="button"
            >
              {/* <Icons.plus size={14} strokeWidth={2} /> */}
              Add new field
            </button>
          </div>
        </div>
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
  schema: ModelRow;
  control: ControllerRenderProps<FieldValues, `rows.${number}.${string}`>;
}

const FormFieldSlot = React.memo(({ schema, control }: FormFieldSlotProps) => {
  switch (schema.fieldType) {
    case "input":
      return (
        <Input
          className={schema.className}
          {...control}
          {...(schema.attrs as InputAttrs)}
        />
      );
    case "select": {
      const options = schema.enum as string[];
      return (
        <Select
          onValueChange={control.onChange}
          defaultValue={control.value}
          value={control.value}
        >
          <SelectTrigger className={cn("w-[180px]", schema.className)}>
            <SelectValue placeholder={control.name} />
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
    default:
      return null;
  }
});
