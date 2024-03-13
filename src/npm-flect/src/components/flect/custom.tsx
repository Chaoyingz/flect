import React, { useEffect, useRef, useState } from 'react'

export interface CustomProps {
  componentType: 'custom'
  className?: string
  package: string
  component: string
  uri: string
}

interface UseDynamicComponentOptions<P = unknown> {
  onCompleted?: (name: string, Component: React.ComponentType<P> | undefined) => void
  onError?: (err: Error) => void
}

function useDynamicComponentImport<P = unknown>(
  uri: string,
  component: string,
  options: UseDynamicComponentOptions<P> = {},
) {
  const ImportedComponentRef = useRef<React.ComponentType<P>>()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error>()

  const { onCompleted, onError } = options
  useEffect(() => {
    setLoading(true)
    const importComponent = async (): Promise<void> => {
      try {
        ImportedComponentRef.current = (await import(uri))[component]
        onCompleted?.(component, ImportedComponentRef.current)
      } catch (err) {
        onError?.(err as Error)
        setError(err as Error)
      } finally {
        setLoading(false)
      }
    }
    importComponent()
  }, [uri, component, onCompleted, onError])

  return { error, loading, Component: ImportedComponentRef.current }
}

export const Custom = (props: CustomProps) => {
  const { error, loading, Component } = useDynamicComponentImport<CustomProps>(props.uri, props.component)
  console.log('Component', Component)
  if (error) {
    return <div>Error: {error.message}</div>
  } else if (loading) {
    return <div>Loading...</div>
  } else if (Component) {
    return <Component {...props} />
  }
}
