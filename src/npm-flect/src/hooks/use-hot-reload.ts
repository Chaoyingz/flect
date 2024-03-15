import { useEffect } from "react";

export function useHotReload() {
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
