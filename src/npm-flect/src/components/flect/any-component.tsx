import { Avatar, AvatarProps } from '@/components/flect/avatar'
import { Button, ButtonProps } from '@/components/flect/button'
import { Container, ContainerProps } from '@/components/flect/container'
import { Heading, HeadingProps } from '@/components/flect/heading'
import { Link, LinkProps } from '@/components/flect/link'
import { Text, TextProps } from '@/components/flect/text'
import { Table, TableProps } from '@/components/flect/table'
import { Outlet, OutletProps } from '@/components/flect/outlet'
import { Form, FormProps } from '@/components/flect/form'
import { NavLink, NavLinkProps } from '@/components/flect/nav-link'
import { Paragraph, ParagraphProps } from '@/components/flect/paragraph'
import { Markdown, MarkdownProps } from '@/components/flect/markdown'
import { CopyButton, CopyButtonProps } from '@/components/flect/copy-button'
import { CodeBlock, CodeBlockProps } from '@/components/flect/code-block'
import { Custom, CustomProps } from '@/components/flect/custom'

export type ComponentProps =
  | AvatarProps
  | ButtonProps
  | CodeBlockProps
  | ContainerProps
  | CopyButtonProps
  | CustomProps
  | FormProps
  | HeadingProps
  | LinkProps
  | MarkdownProps
  | NavLinkProps
  | OutletProps
  | ParagraphProps
  | TableProps
  | TextProps

export function AnyComponent(props: ComponentProps) {
  const { componentType } = props
  switch (componentType) {
    case 'avatar':
      return <Avatar {...props} />
    case 'button':
      return <Button {...props} />
    case 'code-block':
      return <CodeBlock {...props} />
    case 'container':
      return <Container {...props} />
    case 'copy-button':
      return <CopyButton {...props} />
    case 'custom':
      return <Custom {...props} />
    case 'form':
      return <Form {...props} />
    case 'heading':
      return <Heading {...props} />
    case 'link':
      return <Link {...props} />
    case 'markdown':
      return <Markdown {...props} />
    case 'nav-link':
      return <NavLink {...props} />
    case 'outlet':
      return <Outlet />
    case 'paragraph':
      return <Paragraph {...props} />
    case 'table':
      return <Table {...props} />
    case 'text':
      return <Text {...props} />
  }
}

export function AnyComponents({ children }: { children?: ComponentProps[] }) {
  return <>{children && children.map((props, index) => <AnyComponent key={index} {...props} />)}</>
}
