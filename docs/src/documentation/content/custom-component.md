# Custom Component Integration in Flect

Integrating custom components into Flect significantly enhances the framework's capabilities. By incorporating your own React components, you can tailor Flect's functionality to meet your specific needs.

## Flect's Frontend Ecosystem

Flect's frontend ecosystem comprises two primary packages:

- **The Flect Component Library:** This package includes all of Flect's built-in components.
- **Prebuilt:** This package is specifically designed for rendering page logic as a React application.

This structure promotes modularity and customization, allowing you to adjust the default styles and logic of Flect components as needed.

## Guide Overview

This guide outlines the steps to implement custom components by creating your own prebuilt package. We will demonstrate this process by developing a simple badge component.

## Implementing Custom Components: A Step-by-Step Guide

### 1. Project Structure Setup

Begin by creating the project structure and installing necessary dependencies. For a project named "ui", use the Cookiecutter template with the following commands:

```console
cookiecutter https://github.com/Chaoyingz/cookiecutter-flect-prebuilt
cd ui
pnpm install
```

This will set up a project using a standard Vite React-TS template and install the required dependencies.

### 2. Custom Component Development

Develop your custom badge component by editing the `src/components/badge.tsx` file. Insert the following code:

```tsx
import { cn } from '@/lib/utils.ts'

interface BadgeProps {
  package: 'ui'
  type: 'badge'
  subType: 'badge'
  className?: string
  text: string
}

export const Badge = (props: BadgeProps) => {
  return (
    <div
      className={cn(
        'inline-flex rounded-md px-2.5 py-1 text-xs font-semibold bg-primary text-primary-foreground',
        props.className,
      )}
    >
      {props.text}
    </div>
  )
}
```

Ensure to specify the `package`, `type`, and `subType` attributes correctly, with `package` referring to your component's package name and `type` and `subType` referring to the component type.

### 3. `ComponentResolver` Implementation

The `ComponentResolver` locates and renders components in response to backend requests. Implement it in the `src/components/component-resolver.tsx` file as follows:

```tsx
import { BadgeProps, Badge } from '@/components/badge'
import { ComponentResolver } from '@chaoying/flect'

type AnyComponentProps = BadgeProps

export const UIComponentResolver: ComponentResolver = (props: AnyComponentProps) => {
  switch (props.subType) {
    case 'badge':
      return <Badge {...props} />
    default:
      return null
  }
}
UIComponentResolver.package = 'ui'
```

### 4. Integrating the `ComponentResolver`

Update the `src/app.tsx` file to include the `ComponentResolver`:

```tsx
import { Flect, ActionResolverProvider, ComponentResolverProvider } from '@chaoying/flect'
import { UIComponentResolver } from '@/components/component-resolver'

function App() {
  return (
    <ActionResolverProvider resolver={FlectActionResolver}>
      <ComponentResolverProvider resolver={FlectComponentResolver}>
        <ComponentResolverProvider resolver={UIComponentResolver}>
          <Flect />
        </ComponentResolverProvider>
      </ComponentResolverProvider>
    </ActionResolverProvider>
  )
}

export default App
```

### 5. Building the Component

Compile your component package with:

```
pnpm build
```

### 6. Python Integration

Incorporate your component into the Flect Python project by adding the following to a `components.py` file:

```python
from typing import Literal, Optional
from flect import components as c

class BaseUIComponent(c.Custom):
    package: Literal["ui"] = "ui"
    sub_type: Literal["badge"] = "badge"

class Badge(BaseUIComponent):
    class_name: Optional[str] = None
    text: str
```

### 7. Updating prebuilt_uri

Modify `main.py` to update the `prebuilt_uri`:

```python
from flect import flect

from project import app as project_app

app = flect(
    project_app,
    prebuilt_uri={Your dist assets absolute path here e.g "/tmp/ui/dist/assets"},
)
```

### 8. Using the Custom Component

Your custom component is now ready for use within the Flect application, just like any built-in component. For example:

```python
from flect import PageResponse
from components import Badge

async def page():
    return PageResponse(
        body=Badge(text="Hello Badge!"),
    )
```

Upon starting the service, you will see a badge displaying "Hello Badge!" on your webpage.

![custom-badge](https://github.com/Chaoyingz/flect/assets/32626585/a0cf5dec-71a6-4b25-b054-1d9b66916e1d)
