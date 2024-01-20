import { Avatar, AvatarProps } from '@/components/tui/avatar'
import { Button, ButtonProps } from '@/components/tui/button'
import { Container, ContainerProps } from '@/components/tui/container'
import { Logo, LogoProps } from './tui/logo'
import { Heading, HeadingProps } from './tui/heading'
import { Link, LinkProps } from './tui/link'
import { Text, TextProps } from './tui/text'

export type ComponentProps =
  | ButtonProps
  | AvatarProps
  | ContainerProps
  | LogoProps
  | HeadingProps
  | LinkProps
  | TextProps

export function AnyComponentList({ children }: { children?: ComponentProps[] }) {
  return <>{children && children.map((props, index) => <AnyComponent key={index} {...props} />)}</>
}

export function AnyComponent(props: ComponentProps) {
  const { ctype } = props
  switch (ctype) {
    case 'button':
      return <Button {...props} />
    case 'avatar':
      return <Avatar {...props} />
    case 'container':
      return <Container {...props} />
    case 'logo':
      return <Logo {...props} />
    case 'heading':
      return <Heading {...props} />
    case 'link':
      return <Link {...props} />
    case 'text':
      return <Text {...props} />
  }
}
