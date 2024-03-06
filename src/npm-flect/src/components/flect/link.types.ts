import { cva } from 'class-variance-authority'

export const linkVariants = cva('text-primary', {
  variants: {
    underline: {
      none: '',
      hover: 'underline-offset-4 hover:underline',
      always: 'underline-offset-4 underline',
    },
    isActive: {
      true: 'underline-offset-4 underline font-semibold',
      false: '',
    },
  },
  defaultVariants: {
    underline: 'hover',
    isActive: false,
  },
})
