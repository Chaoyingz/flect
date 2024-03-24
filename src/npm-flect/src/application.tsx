import { Router } from "@/components/routing";
import { Toaster } from "@/components/ui/sonner";
import "@/globals.css";
import { ConfigContextState, ConfigProvider } from "@/contexts/config";
import { TooltipProvider } from "@/components/ui/tooltip";

export function Flect(props: ConfigContextState) {
  return (
    <ConfigProvider config={props}>
      <TooltipProvider>
        <Router />
        <Toaster />
      </TooltipProvider>
    </ConfigProvider>
  );
}
