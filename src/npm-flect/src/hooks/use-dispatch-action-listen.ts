import { useEffect, useState } from "react";

export function useDispatchActionListen(event: string) {
  console.log("event", event);
  const [dispatched, setDispatched] = useState(false);
  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    function handleEvent(_: Event) {
      console.log("dispatched");
      setDispatched(true);
    }

    window.addEventListener(event, handleEvent);
    return () => {
      window.removeEventListener(event, handleEvent);
    };
  }, [event]);

  return { dispatched, setDispatched };
}
