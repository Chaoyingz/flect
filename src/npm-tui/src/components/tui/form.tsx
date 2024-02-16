import { useForm, FieldValues, ControllerRenderProps } from 'react-hook-form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import {
  Form as FormUI,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { JSONSchema7, JSONSchema7TypeName } from 'json-schema'
import { ajvResolver } from '@/lib/ajv-resolver'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

export interface FormProps {
  ctype: 'form'
  model: JSONSchema7
}

export function Form(props: FormProps) {
  const form = useForm({
    resolver: ajvResolver(props.model),
  })
  function onSubmit(values: FieldValues) {
    console.log('values', values)
  }
  return (
    <FormUI {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        {props.model.properties &&
          Object.entries(props.model.properties).map(([key, value]) => {
            if (typeof value === 'object' && value !== null && !Array.isArray(value) && 'type' in value) {
              return (
                <FormField
                  key={key}
                  control={form.control}
                  name={key}
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>{key}</FormLabel>
                      <FormControl>
                        <FormFieldSlot type={value.type} enum={value.enum as string[]} field={field} />
                      </FormControl>
                      <FormDescription>{value.description}</FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              )
            }
            return null
          })}

        <Button type="submit">Submit</Button>
      </form>
    </FormUI>
  )
}

interface FormFieldSlotProps {
  type: JSONSchema7TypeName | JSONSchema7TypeName[] | undefined
  enum?: string[]
  field: ControllerRenderProps
}

function FormFieldSlot({ type, enum: enumValues, field }: FormFieldSlotProps) {
  if (enumValues) {
    return (
      <Select onValueChange={field.onChange} defaultValue={field.value} value={field.value}>
        <SelectTrigger className="w-[180px]">
          <SelectValue placeholder={field.name} />
        </SelectTrigger>
        <SelectContent>
          {enumValues.map((value) => (
            <SelectItem key={value} value={value}>
              {value}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    )
  } else {
    switch (type) {
      case 'string':
      case 'number':
        return <Input {...field} type="number" />
      case 'integer':
        return <Input {...field} type="integer" />
      case 'boolean':
        return <Input {...field} type="checkbox" />
      default:
        return <Input {...field} />
    }
  }
}
