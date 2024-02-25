import { lazy } from 'react'
import { FormLazyProps } from '@/components/tui/form-lazy'

export type { FormLazyProps as FormProps }

export const Form = lazy(() => import('./form-lazy'))
