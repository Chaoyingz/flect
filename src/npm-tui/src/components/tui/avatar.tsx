import { AvatarFallback, AvatarImage, Avatar as AvatarUI } from '@/components/ui/avatar'

export interface AvatarProps {
  ctype: 'avatar'
  src?: string
  alt?: string
  fallback: string
}
export function Avatar(props: AvatarProps) {
  return (
    <AvatarUI>
      <AvatarImage src={props.src} alt={props.alt} />
      <AvatarFallback>{props.fallback}</AvatarFallback>
    </AvatarUI>
  )
}
