import { lazy } from 'react'
import { FormLazyProps } from '@/components/flect/form-lazy'

export type { FormLazyProps as FormProps }

export const Form = lazy(() => import('./form-lazy'))
