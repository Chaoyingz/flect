import { Avatar, AvatarProps } from '@/components/tui/avatar'
import { Button, ButtonProps } from '@/components/tui/button'
import { Container, ContainerProps } from '@/components/tui/container'
import { Heading, HeadingProps } from '@/components/tui/heading'
import { Link, LinkProps } from '@/components/tui/link'
import { Text, TextProps } from '@/components/tui/text'
import { Table, TableProps } from '@/components/tui/table'
import { Outlet, OutletProps } from '@/components/tui/outlet'
import { Form, FormProps } from '@/components/tui/form'

export type ComponentProps =
  | AvatarProps
  | ButtonProps
  | ContainerProps
  | FormProps
  | HeadingProps
  | LinkProps
  | OutletProps
  | TableProps
  | TextProps

export function AnyComponent(props: ComponentProps) {
  const { componentType } = props
  switch (componentType) {
    case 'avatar':
      return <Avatar {...props} />
    case 'button':
      return <Button {...props} />
    case 'container':
      return <Container {...props} />
    case 'form':
      return <Form {...props} />
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

export function AnyComponents({ children }: { children?: ComponentProps[] }) {
  return <>{children && children.map((props, index) => <AnyComponent key={index} {...props} />)}</>
}
