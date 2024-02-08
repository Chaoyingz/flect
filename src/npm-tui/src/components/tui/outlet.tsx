import { Outlet as RemixOutlet } from 'react-router-dom'

export interface OutletProps {
  ctype: 'outlet'
}

export function Outlet() {
  return <RemixOutlet />
}
