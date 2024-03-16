import {
  Flect,
  ActionResolverProvider,
  ComponentResolverProvider,
  components,
} from "@chaoying/flect";

function App() {
  return (
    <ActionResolverProvider resolver={components.FlectActionResolver}>
      <ComponentResolverProvider resolver={components.FlectComponentResolver}>
        <Flect />
      </ComponentResolverProvider>
    </ActionResolverProvider>
  );
}

export default App;
