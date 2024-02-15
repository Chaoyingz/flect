import { useForm, FieldValues } from 'react-hook-form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { SchemaObject } from 'ajv'
import {
  Form as FormUI,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { ajvResolver } from '@/lib/ajv-resolver'

export interface FormProps {
  ctype: 'form'
  model: SchemaObject
}
export function Form(props: FormProps) {
  console.log(props)

  const form = useForm({
    resolver: ajvResolver(props.model),
  })
  function onSubmit(values: FieldValues) {
    console.log('values', values)
  }
  return (
    <FormUI {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Username</FormLabel>
              <FormControl>
                <Input placeholder="shadcn" {...field} />
              </FormControl>
              <FormDescription>This is your public display name.</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </FormUI>
  )
}
