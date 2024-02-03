import {
  createBrowserRouter,
  RouteObject,
  RouterProvider,
  useLoaderData,
  useRouteError,
  RouteProps as RemixRouteProps,
} from 'react-router-dom'
import { useEffect, useState } from 'react'
import { AnyComponents, ComponentProps } from '@/components/tui/any-component'

export type RouteProps = RemixRouteProps & {
  children?: RouteProps[]
  segment: string
  pathname: string
  endpoint: 'layout' | 'page'
}

function RouteElement() {
  const components = useLoaderData() as ComponentProps[]
  return <AnyComponents children={components} />
}

function ErrorElement() {
  const error = useRouteError() as { statusText?: string; message?: string }
  console.error(error)

  return (
    <div className="flex min-h-screen flex-col items-center justify-center text-center">
      <div>
        <h1 className="text-4xl font-medium mb-6">Oops!</h1>
        <p className="mb-6">Sorry, an unexpected error has occurred.</p>
        <p>
          <i>{error.statusText || error.message}</i>
        </p>
      </div>
    </div>
  )
}

async function routeLoader({ request }: { request: Request }): Promise<ComponentProps[]> {
  const response = await fetch('/tui' + new URL(request.url).pathname)
  return await response.json()
}

async function layoutLoader(pathname: string): Promise<ComponentProps[]> {
  const response = await fetch(`/tui${pathname}_layout`)
  return await response.json()
}

function parseRoute(routes: RouteProps[]): RouteObject[] {
  function converter(route: RouteProps): RouteObject {
    const routeObj: RouteObject = {
      path: route.segment,
      element: <RouteElement />,
      errorElement: <ErrorElement />,
      loader: route.endpoint === 'layout' ? () => layoutLoader(route.pathname) : routeLoader,
      index: route.index,
    }

    if (route.children && route.children.length > 0) {
      routeObj.children = route.children.map(converter)
    }

    return routeObj
  }
  return routes.map(converter)
}

async function getRouteObject(): Promise<RouteObject[]> {
  const response = await fetch('/tui/_route')
  const routeProps = (await response.json()) as RouteProps[]
  return await parseRoute(routeProps)
}

export function Router() {
  const [routeObjs, setRouteObjs] = useState<RouteObject[]>()
  useEffect(() => {
    let ignore = false
    async function fetchComponents() {
      if (ignore) {
        return
      }
      setRouteObjs(await getRouteObject())
    }
    fetchComponents()
    return () => {
      ignore = true
    }
  }, [])
  return routeObjs ? <RouterProvider router={createBrowserRouter(routeObjs)} /> : null
}
