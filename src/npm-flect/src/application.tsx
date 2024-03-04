import { useEffect } from 'react'
import { Router } from './routing'
import { Toaster } from '@/components/ui/sonner'

function useHotReload() {
  useEffect(() => {
    const source = new EventSource('/_hotreload')

    source.onmessage = function (event) {
      if (event.data === 'reload') {
        source.close()
        window.location.reload()
      }
    }

    return () => {
      source.close()
    }
  }, [])
}

function App() {
  useHotReload()
  return (
    <>
      <Router />
      <Toaster richColors />
    </>
  )
}

export default App
