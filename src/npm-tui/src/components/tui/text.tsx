export interface TextProps {
  ctype: 'text'
  className?: string
  text: string
}

export function Text(props: TextProps) {
  const { text } = props
  return <>{text}</>
}
