import {
  Flect,
  ActionResolverProvider,
  ComponentResolverProvider,
} from "@chaoying/flect";
import {
  FlectActionResolver,
  FlectComponentResolver,
} from "@chaoying/flect/components";

function App() {
  return (
    <ActionResolverProvider resolver={FlectActionResolver}>
      <ComponentResolverProvider resolver={FlectComponentResolver}>
        <Flect />
      </ComponentResolverProvider>
    </ActionResolverProvider>
  );
}

export default App;
