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
import { Display, DisplayType } from "@/components/flect/display";

export interface Dataset {
  [k: string]: Json;
}

interface Model extends JSONSchema7 {
  displayType: DisplayType;
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
            {Object.keys(props.model.properties).map((key, index) => {
              return (
                <TableCell key={index}>
                  <Display
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
