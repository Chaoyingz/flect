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

function App() {
  return (
    <ActionResolverProvider resolver={FlectActionResolver}>
      <ComponentResolverProvider resolver={FlectComponentResolver}>
        <Flect
          debug={
            Boolean(getMetaContent("flect:debug")) ||
            process.env.NODE_ENV === "development"
          }
        />
      </ComponentResolverProvider>
    </ActionResolverProvider>
  );
}

export default App;
