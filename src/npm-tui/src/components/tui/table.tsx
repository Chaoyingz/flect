import { Table as TableUI, TableHead, TableBody, TableRow, TableCell, TableHeader } from '@/components/ui/table'
import { Json } from '@/types'

export interface Dataset {
  [k: string]: Json
}

export interface TableProps {
  ctype: 'table'
  className?: string

  labels: string[]
  datasets: Dataset[]
}

export function Table(props: TableProps) {
  return (
    <TableUI>
      <TableHeader>
        <TableRow>
          {props.labels.map((label, index) => (
            <TableHead key={index}>{label}</TableHead>
          ))}
        </TableRow>
      </TableHeader>
      <TableBody>
        {props.datasets.map((dataset, index) => (
          <TableRow key={index}>
            {props.labels.map((label, index) => (
              <TableCell key={index}>
                <Cell value={dataset[label]} />
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </TableUI>
  )
}

function Cell({ value }: { value: Json }) {
  return <>{value}</>
}
