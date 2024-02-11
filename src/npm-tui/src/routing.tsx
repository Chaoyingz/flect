import {
  createBrowserRouter,
  RouteObject,
  RouterProvider,
  useLoaderData,
  useRouteError,
  LoaderFunctionArgs,
  useNavigate,
  RouteProps as RemixRouteProps,
} from 'react-router-dom'
import { useCallback, useEffect, useState } from 'react'
import { AnyComponent, ComponentProps } from '@/components/tui/any-component'
import React from 'react'
import { Button } from './components/ui/button'

const LAYOUT_ENDPOINT_NAME = 'layout'

const ROOT_ROUTER_PREFIX = '/tui'
const ROUTE_ROUTER_PATH = '/_route/'
const LAYOUT_ROUTER_SUFFIX = '_layout/'

export type RouteProps = RemixRouteProps & {
  children?: RouteProps[]
  segment: string
  pathname: string
  endpoint: 'layout' | 'page'
}

const RouteElement = React.memo(() => {
  const component = useLoaderData() as ComponentProps
  return <AnyComponent {...component} />
})

const ErrorElement = React.memo(() => {
  const error = useRouteError() as { statusText?: string; message?: string }
  const navigate = useNavigate()
  console.error(error)

  return (
    <div className="flex min-h-screen flex-col items-center justify-center text-center">
      <div>
        <h1 className="text-4xl font-medium mb-6">Oops!</h1>
        <p className="mb-6">Sorry, an unexpected error has occurred.</p>
        <p>
          <i>{error.statusText || error.message}</i>
        </p>
        <Button size={'sm'} className="mt-6" onClick={() => navigate(-1)}>
          Go Back
        </Button>
      </div>
    </div>
  )
})

interface DefaultResponse {
  [key: string]: unknown
}

const fetchJson = async <T = DefaultResponse,>(input: RequestInfo, init?: RequestInit): Promise<T> => {
  const response = await fetch(input, init)
  if (!response.ok) {
    throw new Error(response.statusText)
  }
  return await response.json()
}

const useRoutes = () => {
  const [routes, setRoutes] = useState<RouteObject[] | undefined>()

  const convertRoute = useCallback((route: RouteProps): RouteObject => {
    const path = route.pathname.replace(/{(.*?)}/g, ':$1')
    const loader = async ({ params }: LoaderFunctionArgs) => {
      let endpointPath = `${ROOT_ROUTER_PREFIX}${path}`
      if (route.endpoint === LAYOUT_ENDPOINT_NAME) {
        endpointPath += LAYOUT_ROUTER_SUFFIX
      }

      Object.keys(params).forEach((key) => {
        const value = params[key]
        if (value) {
          endpointPath = endpointPath.replace(`:${key}`, value)
        }
      })

      return fetchJson<ComponentProps[]>(endpointPath)
    }

    return {
      path: path,
      element: <RouteElement />,
      errorElement: <ErrorElement />,
      loader,
      children: route.children?.map(convertRoute),
    }
  }, [])

  useEffect(() => {
    let isMounted = true

    fetchJson<RouteProps[]>(`${ROOT_ROUTER_PREFIX}${ROUTE_ROUTER_PATH}`)
      .then((routeProps) => {
        if (isMounted) {
          setRoutes(routeProps.map(convertRoute))
        }
      })
      .catch(console.error)

    return () => {
      isMounted = false
    }
  }, [])

  return routes
}

export const Router = () => {
  const routeObjects = useRoutes()
  return routeObjects ? <RouterProvider router={createBrowserRouter(routeObjects)} /> : null
}
