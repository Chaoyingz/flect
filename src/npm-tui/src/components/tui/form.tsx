import { useForm, FieldValues, ControllerRenderProps } from 'react-hook-form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import {
  Form as FormUI,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { JSONSchema7 } from 'json-schema'
import { Textarea } from '@/components/ui/textarea'
import { ajvResolver } from '@/lib/ajv-resolver'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { cn } from '@/lib/utils'
import React from 'react'

interface InputAttrs {
  type: 'text' | 'password' | 'email'
  placeholder?: string
}

interface TextAreaAttrs {
  rows?: number
  cols?: number
  placeholder?: string
}

interface SelectAttrs {
  options: string[]
}

type FieldCtype = 'checkbox' | 'input' | 'select' | 'textarea'
type FieldAttrs = InputAttrs | TextAreaAttrs | SelectAttrs

interface Model extends JSONSchema7 {
  ctype: FieldCtype
  class_name?: string
  attrs?: FieldAttrs
  properties: {
    [key: string]: Model
  }
}

export interface FormProps {
  ctype: 'form'
  model: Model
}

function getDefaultValues(schema: Model): FieldValues {
  const defaults: FieldValues = {}
  Object.keys(schema.properties).forEach((key) => {
    const prop = schema.properties[key]
    if (prop.default !== undefined) {
      defaults[key] = prop.default
    }
  })
  return defaults
}

export function Form(props: FormProps) {
  console.log('props', props)
  const form = useForm({
    resolver: ajvResolver(props.model),
    defaultValues: getDefaultValues(props.model),
  })
  function onSubmit(values: FieldValues) {
    console.log('values', values)
  }
  return (
    <FormUI {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        {props.model.properties &&
          Object.entries(props.model.properties).map(([key, value]) => {
            let modifiedAttrs = value.attrs
            if (value.ctype === 'select' && value.enum) {
              modifiedAttrs = {
                ...value.attrs,
                options: value.enum as string[],
              }
            }
            if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
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
                          ctype={value.ctype}
                          attrs={modifiedAttrs}
                          field={field}
                          className={value.class_name}
                        />
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
  ctype: FieldCtype
  attrs?: FieldAttrs
  className?: string
  field: ControllerRenderProps
}

const FormFieldSlot = React.memo(({ ctype, attrs, field, className }: FormFieldSlotProps) => {
  switch (ctype) {
    case 'checkbox':
      return <Checkbox className={className} {...field} />
    case 'input':
      return <Input className={className} {...field} {...(attrs as InputAttrs)} />
    case 'select': {
      const { options } = attrs as SelectAttrs
      return (
        <Select onValueChange={field.onChange} defaultValue={field.value} value={field.value}>
          <SelectTrigger className={cn('w-[180px]', className)}>
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
      )
    }
    case 'textarea':
      return <Textarea className={className} {...field} {...(attrs as TextAreaAttrs)} />
    default:
      return null
  }
})
