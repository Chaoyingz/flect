export interface TextProps {
  ctype: 'text'
  className?: string
  text: string
}

export function Text(props: TextProps) {
  const { text, className } = props
  return <>{className ? <span className={className}>{text}</span> : <>{text}</>}</>
}
