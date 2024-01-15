export interface TextProps {
  ctype: 'text'
  text: string
}

export function Text(props: TextProps) {
  const { text } = props
  return <>{text}</>
}
