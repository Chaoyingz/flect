export interface ParagraphProps {
  componentType: 'paragraph'
  className?: string
  text: string
}

export function Paragraph(props: ParagraphProps) {
  const { text, className } = props
  return <p className={className}>{text}</p>
}
