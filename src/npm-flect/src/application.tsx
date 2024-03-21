import { Router } from "@/components/routing";
import { Toaster } from "@/components/ui/sonner";
import "@/globals.css";
import { ConfigContextState, ConfigProvider } from "@/contexts/config";

export function Flect(props: ConfigContextState) {
  return (
    <ConfigProvider config={props}>
      <Router />
      <Toaster />
    </ConfigProvider>
  );
}
