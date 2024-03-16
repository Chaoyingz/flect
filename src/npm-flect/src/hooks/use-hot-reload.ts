import { useEffect } from "react";

export function useHotReload() {
  useEffect(() => {
    if (process.env.NODE_ENV === "production") {
      return;
    }

    const source = new EventSource("/_hotreload");

    source.onmessage = (event) => {
      if (event.data === "reload") {
        source.close();
        window.location.reload();
      }
    };

    return () => source.close();
  }, []);
}
