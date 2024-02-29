import { toast } from 'sonner'

type Notify = {
  actionType: 'notify'
  title: string
  description?: string
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'top-center' | 'bottom-center'
  type: 'normal' | 'action' | 'success' | 'info' | 'warning' | 'error' | 'loading' | 'default'
}

type AnyAction = Notify

export type ActionResponse = {
  action: AnyAction
}

export function executeAction(action: AnyAction) {
  switch (action.actionType) {
    case 'notify': {
      const { title, type } = action as Notify
      switch (type) {
        case 'success':
          toast.success(title, action)
          break
        case 'info':
          toast.info(title, action)
          break
        case 'warning':
          toast.warning(title, action)
          break
        case 'error':
          toast.error(title, action)
          break
        default:
          toast(title, action)
      }
    }
  }
}
