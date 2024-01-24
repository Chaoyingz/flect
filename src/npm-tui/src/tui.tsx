import { AnyComponents, ComponentProps } from './components/any-component'
import { useEffect, useState } from 'react'

type TuiProps = {
  rootUrl: string
}

export function Tui({ rootUrl }: TuiProps) {
  const url = rootUrl + window.location.pathname
  return <Fetch url={url} />
}

type FetchProps = {
  url: string
}

function Fetch({ url }: FetchProps) {
  const [components, setComponents] = useState<ComponentProps[]>([])

  useEffect(() => {
    let ignore = false
    async function fetchComponents() {
      if (ignore) {
        return
      }
      const response = await fetch(url)
      const data = await response.json()
      setComponents(data)
    }
    fetchComponents()
    return () => {
      ignore = true
    }
  }, [url])
  return <Render children={components} />
}

function Render(params: { children: ComponentProps[] }) {
  return <AnyComponents children={params.children} />
}
