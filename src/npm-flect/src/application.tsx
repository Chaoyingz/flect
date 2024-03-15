import { Router } from "@/components/routing";
import { Toaster } from "@/components/ui/sonner";
import { useHotReload } from "@/hooks/use-hot-reload";
import "@/globals.css";

export function Flect() {
  useHotReload();
  return (
    <>
      <Router />
      <Toaster />
    </>
  );
}
