import { cn } from '@/lib/utils'
import { AnyComponents, ComponentProps } from '@/components/flect/any-component'
import { NavLink as RemixNavLink } from 'react-router-dom'

export interface NavLinkProps {
  componentType: 'nav-link'
  className?: string
  href: string
  text: string
  children?: ComponentProps[]
}

export function NavLink(props: NavLinkProps) {
  const { href, children } = props
  return (
    <RemixNavLink
      to={href}
      className={({ isActive }) =>
        isActive
          ? cn('text-primary underline-offset-4 hover:underline font-semibold', props.className)
          : cn('text-primary underline-offset-4 hover:underline', props.className)
      }
    >
      <AnyComponents children={children} />
    </RemixNavLink>
  )
}
