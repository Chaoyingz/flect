import { Outlet as RemixOutlet } from "react-router-dom";

export interface OutletProps {
  package: "flect";
  type: "outlet";
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export function Outlet(_: OutletProps) {
  return <RemixOutlet />;
}
