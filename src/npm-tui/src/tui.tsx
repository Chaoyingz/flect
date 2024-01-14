import { AnyComponentList, ComponentProps } from './components/any-component'
import { useEffect, useState } from 'react'

type TuiProps = {
  rootUrl: string
}

export function Tui({ rootUrl = '/api' }: TuiProps) {
  return <Fetch url={rootUrl} />
}

type FetchProps = {
  url: string
}

function Fetch({ url }: FetchProps) {
  const [propsList, setPropsList] = useState<ComponentProps[]>([])

  useEffect(() => {
    async function fetchComponents() {
      const response = await fetch(url)
      const data = await response.json()
      console.log(data)
      setPropsList(data)
    }
    fetchComponents()
  }, [])
  return <Render propsList={propsList} />
}

function Render(params: { propsList: ComponentProps[] }) {
  return <AnyComponentList propsList={params.propsList} />
}
