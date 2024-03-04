import { Outlet as RemixOutlet } from 'react-router-dom'

export interface OutletProps {
  componentType: 'outlet'
}

export function Outlet() {
  return <RemixOutlet />
}
