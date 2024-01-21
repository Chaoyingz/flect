import { cn } from '@/lib/utils'
import { AnyComponents, ComponentProps } from '../any-component'

export interface LinkProps {
  ctype: 'link'
  className?: string
  href: string
  text: string
  children?: ComponentProps[]
}

export function Link(props: LinkProps) {
  const { href, children } = props
  return (
    <a href={href} className={cn('text-primary underline-offset-4 hover:underline')}>
      <AnyComponents children={children} />
    </a>
  )
}
