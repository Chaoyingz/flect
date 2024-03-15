import { Router } from "@/routing";
import { Toaster } from "@/components/ui/sonner";
import "@/globals.css";
import { useHotReload } from "@/hooks/use-hot-reload";

export function Flect() {
  useHotReload();
  return (
    <>
      <Router />
      <Toaster />
    </>
  );
}
