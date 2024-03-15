import { Flect, resolver } from "@chaoying/flect";

function App() {
  return (
    <resolver.ResolverProvider resolver={resolver.FlectComponentResolver}>
      <Flect />
    </resolver.ResolverProvider>
  );
}

export default App;
