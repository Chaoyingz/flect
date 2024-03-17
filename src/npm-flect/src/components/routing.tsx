import {
  createBrowserRouter,
  RouteObject,
  RouterProvider,
  useLoaderData,
  useRouteError,
  LoaderFunctionArgs,
  useNavigate,
  RouteProps as RemixRouteProps,
} from "react-router-dom";
import { useCallback, useEffect, useState } from "react";
import React from "react";
import { Button } from "@/components/ui/button";
import { AnyComponentProps } from "@/types";
import { AnyComponent } from "@/components/flect/any-component";

const CLIENT_ROOT_ROUTER_PREFIX = "/flect";
const CLIENT_ROUTE_ROUTER_PATH = "/_route/";

export type RouteProps = RemixRouteProps & {
  children?: RouteProps[];
  segment: string;
  path: string;
  url: string;
  index: boolean;
};

type PageResponse = {
  body: AnyComponentProps;
};

const RouteElement = React.memo(() => {
  const response = useLoaderData() as PageResponse;
  return <AnyComponent {...response.body} />;
});

const ErrorElement = React.memo(() => {
  const error = useRouteError() as { statusText?: string; message?: string };
  const navigate = useNavigate();
  console.error(error);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center text-center">
      <div>
        <h1 className="mb-6 text-4xl font-medium">Oops!</h1>
        <p className="mb-6">Sorry, an unexpected error has occurred.</p>
        <p>
          <i>{error.statusText || error.message}</i>
        </p>
        <Button size={"sm"} className="mt-6" onClick={() => navigate(-1)}>
          Go Back
        </Button>
      </div>
    </div>
  );
});

interface DefaultPageResponse {
  [key: string]: unknown;
}

const fetchJson = async <T = DefaultPageResponse,>(
  input: RequestInfo,
  init?: RequestInit,
): Promise<T> => {
  const response = await fetch(input, init);
  if (!response.ok) {
    throw new Error(response.statusText);
  }
  return await response.json();
};

const useRoutes = () => {
  const [routes, setRoutes] = useState<RouteObject[] | undefined>();

  const convertRoute = useCallback((route: RouteProps): RouteObject => {
    const path = route.path.replace(/{(.*?)}/g, ":$1");
    const loader = async ({ params }: LoaderFunctionArgs) => {
      let url = `${CLIENT_ROOT_ROUTER_PREFIX}${route.url.replace(/{(.*?)}/g, ":$1")}`;

      Object.keys(params).forEach((key) => {
        const value = params[key];
        if (value) {
          url = url.replace(`:${key}`, value);
        }
      });
      return fetchJson<AnyComponentProps[]>(url);
    };
    const routeObj: Partial<RouteObject> = {
      path: path,
      element: <RouteElement />,
      errorElement: <ErrorElement />,
      loader,
    };
    if (route.index === true) {
      routeObj.index = true;
    } else {
      routeObj.children = route.children?.map(convertRoute);
    }
    return routeObj;
  }, []);

  useEffect(() => {
    let isMounted = true;

    fetchJson<RouteProps[]>(
      `${CLIENT_ROOT_ROUTER_PREFIX}${CLIENT_ROUTE_ROUTER_PATH}`,
    )
      .then((routeProps) => {
        if (isMounted) {
          setRoutes(routeProps.map(convertRoute));
        }
      })
      .catch(console.error);

    return () => {
      isMounted = false;
    };
  }, [convertRoute]);

  return routes;
};

export const Router = () => {
  const routeObjects = useRoutes();
  return routeObjects ? (
    <RouterProvider router={createBrowserRouter(routeObjects)} />
  ) : null;
};
