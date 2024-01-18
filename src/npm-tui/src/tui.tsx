import { AnyComponentList, ComponentProps } from './components/any-component'
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
  const [propsList, setPropsList] = useState<ComponentProps[]>([])

  useEffect(() => {
    let ignore = false
    async function fetchComponents() {
      if (ignore) {
        return
      }
      const response = await fetch(url)
      const data = await response.json()
      setPropsList(data)
    }
    fetchComponents()
    return () => {
      ignore = true
    }
  }, [url])
  return <Render propsList={propsList} />
}

function Render(params: { propsList: ComponentProps[] }) {
  return <AnyComponentList propsList={params.propsList} />
}
