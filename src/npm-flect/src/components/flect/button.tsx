import { Button as ButtonUI, ButtonProps as ButtonPropsUI } from '@/components/ui/button'
import { AnyComponents, ComponentProps } from '@/components/flect/any-component'

export interface ButtonProps extends Omit<ButtonPropsUI, 'children'> {
  componentType: 'button'
  className?: string
  children?: ComponentProps[]
}

export function Button(props: ButtonProps) {
  const { children } = props
  return (
    <ButtonUI {...props}>
      <AnyComponents children={children} />
    </ButtonUI>
  )
}
