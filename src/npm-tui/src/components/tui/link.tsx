import { cn } from '@/lib/utils'

export interface LinkProps {
  ctype: 'link'
  href: string
  text: string
  className?: string
}

export function Link(props: LinkProps) {
  const { href, text, className } = props
  return (
    <a href={href} className={cn('text-primary underline-offset-4 hover:underline', className)}>
      {text}
    </a>
  )
}
