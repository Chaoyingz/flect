import { lazy } from 'react'
import { CodeBlockLazyProps } from '@/components/flect/code-block-lazy'

export type { CodeBlockLazyProps as CodeBlockProps }

export const CodeBlock = lazy(() => import('./code-block-lazy.tsx'))
