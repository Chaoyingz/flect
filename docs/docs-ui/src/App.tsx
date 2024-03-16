import {
  Flect,
  ActionResolverProvider,
  ComponentResolverProvider,
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
          <Flect />
        </ComponentResolverProvider>
      </ComponentResolverProvider>
    </ActionResolverProvider>
  );
}

export default App;
