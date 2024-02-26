import { lazy } from 'react'
import { MarkdownLazyProps } from '@/components/tui/markdown-lazy'

export type { MarkdownLazyProps as MarkdownProps }

export const Markdown = lazy(() => import('./markdown-lazy.tsx'))
