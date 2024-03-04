import { cn } from '@/lib/utils'
import { AnyComponents, ComponentProps } from '@/components/flect/any-component'
import { Link as RemixLink } from 'react-router-dom'

export interface LinkProps {
  componentType: 'link'
  className?: string
  href: string
  text: string
  children?: ComponentProps[]
}

export function Link(props: LinkProps) {
  const { href, children } = props
  return (
    <RemixLink to={href} className={cn('text-primary underline-offset-4 hover:underline', props.className)}>
      <AnyComponents children={children} />
    </RemixLink>
  )
}
