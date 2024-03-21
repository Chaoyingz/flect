import {
  Flect,
  ActionResolverProvider,
  ComponentResolverProvider,
  getMetaContent,
} from "@chaoying/flect";
import {
  FlectActionResolver,
  FlectComponentResolver,
} from "@chaoying/flect/components";
import { DocsUIComponentResolver } from "@/component-resolver";

function App() {
  return (
    <ActionResolverProvider resolver={FlectActionResolver}>
      <ComponentResolverProvider resolver={FlectComponentResolver}>
        <ComponentResolverProvider resolver={DocsUIComponentResolver}>
          <Flect debug={Boolean(getMetaContent("flect:debug"))} />
        </ComponentResolverProvider>
      </ComponentResolverProvider>
    </ActionResolverProvider>
  );
}

export default App;
