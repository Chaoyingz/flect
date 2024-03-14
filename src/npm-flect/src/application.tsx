import { createContext, useEffect } from "react";
import { Router } from "./routing";
import { Toaster } from "@/components/ui/sonner";
import { ComponentProps } from "./components/flect/any-component";
import "./globals.css";

function useHotReload() {
  useEffect(() => {
    const source = new EventSource("/_hotreload");

    source.onmessage = function (event) {
      if (event.data === "reload") {
        source.close();
        window.location.reload();
      }
    };

    return () => {
      source.close();
    };
  }, []);
}

export type customComponent = (props: ComponentProps) => JSX.Element;

export interface FlectProps {
  customComponent?: customComponent;
}

export const ConfigContext = createContext<FlectProps>({});

export function Flect(props: FlectProps) {
  useHotReload();
  return (
    <ConfigContext.Provider value={props}>
      <Router />
      <Toaster />
    </ConfigContext.Provider>
  );
}
