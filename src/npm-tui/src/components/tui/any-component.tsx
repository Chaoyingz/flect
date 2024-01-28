import { Avatar, AvatarProps } from '@/components/tui/avatar'
import { Button, ButtonProps } from '@/components/tui/button'
import { Container, ContainerProps } from '@/components/tui/container'
import { Heading, HeadingProps } from '@/components/tui/heading'
import { Link, LinkProps } from '@/components/tui/link'
import { Text, TextProps } from '@/components/tui/text'
import { Table, TableProps } from '@/components/tui/table'
import { Outlet, OutletProps } from '@/components/tui/outlet'

export type ComponentProps =
  | AvatarProps
  | ButtonProps
  | ContainerProps
  | HeadingProps
  | LinkProps
  | OutletProps
  | TableProps
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
    case 'outlet':
      return <Outlet />
    case 'table':
      return <Table {...props} />
    case 'text':
      return <Text {...props} />
  }
}
