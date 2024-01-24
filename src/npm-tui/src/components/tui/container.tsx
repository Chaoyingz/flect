import { AnyComponents, ComponentProps } from '../any-component'

export interface ContainerProps {
  ctype: 'container'
  className?: string
  children?: ComponentProps[]
  tag?: 'div' | 'section' | 'header' | 'footer' | 'main' | 'nav' | 'aside'
}

export function Container(props: ContainerProps) {
  const { children, className, tag } = props
  const Tag = tag || 'div'
  return (
    <Tag className={className}>
      <AnyComponents children={children} />
    </Tag>
  )
}
