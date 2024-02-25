import { cn } from '@/lib/utils'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export interface MarkdownLazyProps {
  componentType: 'markdown'
  className?: string
  text: string
}

export default function Markdown(props: MarkdownLazyProps) {
  const { text, className } = props
  return (
    <ReactMarkdown className={cn('prose', className)} remarkPlugins={[remarkGfm]}>
      {text}
    </ReactMarkdown>
  )
}
