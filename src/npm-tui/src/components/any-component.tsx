import { Avatar, AvatarProps } from '@/components/tui/avatar'
import { Button, ButtonProps } from '@/components/tui/button'
import { Container, ContainerProps } from '@/components/tui/container'
import { Logo, LogoProps } from './tui/logo'
import { Heading, HeadingProps } from './tui/heading'
import { Link, LinkProps } from './tui/link'
import { Text, TextProps } from './tui/text'

export type ComponentProps =
  | AvatarProps
  | ButtonProps
  | ContainerProps
  | HeadingProps
  | LinkProps
  | LogoProps
  | TextProps

export function AnyComponents({ children }: { children?: ComponentProps[] }) {
  return <>{children && children.map((props, index) => <AnyComponent key={index} {...props} />)}</>
}

export function AnyComponent(props: ComponentProps) {
  const { ctype } = props
  switch (ctype) {
    case 'avatar':
      return <Avatar {...props} />
    case 'button':
      return <Button {...props} />
    case 'container':
      return <Container {...props} />
    case 'heading':
      return <Heading {...props} />
    case 'link':
      return <Link {...props} />
    case 'logo':
      return <Logo {...props} />
    case 'text':
      return <Text {...props} />
  }
}
