import {
  createBrowserRouter,
  RouteObject,
  RouterProvider,
  useLoaderData,
  RouteProps as RemixRouteProps,
} from 'react-router-dom'
import { useEffect, useState } from 'react'
import { AnyComponents, ComponentProps } from '@/components/tui/any-component'

export type RouteProps = RemixRouteProps & {
  children?: RouteProps[]
}

function RouteElement() {
  const components = useLoaderData() as ComponentProps[]
  return <AnyComponents children={components} />
}

async function routeLoader({ request }: { request: Request }): Promise<ComponentProps[]> {
  const response = await fetch('http://127.0.0.1:8000/tui' + new URL(request.url).pathname)
  return await response.json()
}

async function layoutLoader(pathname: string): Promise<ComponentProps[]> {
  const response = await fetch(`http://127.0.0.1:8000/tui${pathname}_layout`)
  return await response.json()
}

function parseRoute(route: RouteProps): RouteObject[] {
  const routeObjs: RouteObject[] = []

  function converter(route: RouteProps, parentPath = '') {
    const pathname = route.children ? parentPath + route.path + '/' : parentPath
    const routeObj: RouteObject = {
      path: route.path,
      element: <RouteElement />,
      loader: route.children ? () => layoutLoader(pathname) : routeLoader,
      index: route.index,
    }
    if (route.children && route.children.length > 0) {
      routeObj.children = route.children.map((child) => converter(child, pathname))
    }
    return routeObj
  }

  routeObjs.push(converter(route))
  return routeObjs
}

async function getRouteObject(): Promise<RouteObject[]> {
  const response = await fetch('http://127.0.0.1:8000/tui/_route')
  const routeProps = (await response.json()) as RouteProps
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
