import {
  Table as TableUI,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  TableHeader,
} from "@/components/ui/table";
import { Json } from "@/types";
import { JSONSchema7 } from "json-schema";

export interface Dataset {
  [k: string]: Json;
}

interface Model extends JSONSchema7 {
  displayType: "text" | "boolean";
  properties: {
    [key: string]: Model;
  };
}

export interface TableProps {
  package: "flect";
  type: "table";
  className?: string;

  model: Model;
  datasets: Dataset[];
}

export function Table(props: TableProps) {
  const columns = Object.keys(props.model.properties);
  return (
    <TableUI className={props.className}>
      <TableHeader>
        <TableRow>
          {Object.keys(props.model.properties).map((key, index) => {
            return (
              <TableHead key={index}>
                {props.model.properties[key].title}
              </TableHead>
            );
          })}
        </TableRow>
      </TableHeader>
      <TableBody>
        {props.datasets.map((dataset, index) => (
          <TableRow key={index}>
            {columns.map((key, index) => {
              return (
                <TableCell key={index}>
                  <Cell
                    displayType={props.model.properties[key].displayType}
                    value={dataset[key]}
                  />
                </TableCell>
              );
            })}
          </TableRow>
        ))}
      </TableBody>
    </TableUI>
  );
}

interface CellProps {
  displayType: "text" | "boolean";
  value: Json;
}

function Cell({ displayType, value }: CellProps) {
  switch (displayType) {
    case "text":
      return <TextDisplay value={value} />;
    case "boolean":
      return <BooleanDisplay value={value} />;
    default:
      return <TextDisplay value={value} />;
  }
}

function TextDisplay({ value }: { value: Json }) {
  return <>{value}</>;
}

function BooleanDisplay({ value }: { value: Json }) {
  return <>{value ? "true" : "false"}</>;
}
