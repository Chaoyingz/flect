import { Avatar, AvatarProps } from '@/components/tui/avatar'
import { Button, ButtonProps } from '@/components/tui/button'
import { Container, ContainerProps } from '@/components/tui/container'
import { Logo, LogoProps } from './tui/logo'

export type ComponentProps = ButtonProps | AvatarProps | ContainerProps | LogoProps

export function AnyComponentList({ propsList }: { propsList: ComponentProps[] }) {
  return (
    <>
      {propsList.map((props) => (
        <AnyComponent {...props} key={props.ctype} />
      ))}
    </>
  )
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
  }
}
