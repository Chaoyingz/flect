import { AnyComponentList, ComponentProps } from '../any-component'

export interface ContainerProps {
  ctype: 'container'
  components?: ComponentProps[]
  className?: string
  tag?: 'div' | 'section' | 'header' | 'footer' | 'main' | 'nav' | 'aside'
}

export function Container(props: ContainerProps) {
  const { components, className, tag } = props
  const Tag = tag || 'div'
  return (
    <Tag className={className}>
      <AnyComponentList propsList={components || []} />
    </Tag>
  )
}
