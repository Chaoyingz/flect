# Custom Component Integration in flect

Custom components significantly expand the capabilities of flect by allowing the integration of your own React components into the framework. Not only do they enable you to add new functionalities, but you can also modify the default styles and logic of existing flect components. This guide details the process of implementing custom components through the creation of your own `prebuilt` package, illustrated with the development of a simple badge component.

## Implementing Custom Components: A Step-by-Step Guide

1. **Project Structure Setup**

   Start by establishing the project structure and installing necessary dependencies. For projects named "ui", you can utilize the Cookiecutter template by executing the following commands:

   ```console
   cookiecutter https://github.com/Chaoyingz/cookiecutter-flect-prebuilt
   cd ui
   pnpm install
   ```

   This initializes a project using a standard vite react-ts template and installs the required dependencies.

2. **Custom Component Development**

   To develop your custom badge component, open the `src/components/badge.tsx` file and insert the code below:

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

   Ensure that the `package`, `type`, and `subType` attributes are specified, with `package` referring to your component's package name and `type` to the component type.

3. **`ComponentResolver` Implementation**

   The `ComponentResolver` serves as the mechanism for locating and rendering the appropriate component in response to backend requests. Incorporate the following implementation into the `src/components/component-resolver.tsx` file:

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

   It's crucial to correctly set the `package` attribute here.

4. **Integrating the `ComponentResolver`**

   Update the `src/app.tsx` file to include the newly created `ComponentResolver` as shown below:

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

5. **Building the Component**

   Compile your component package with the following command:

   ```
   pnpm build
   ```

6. **Python Integration**

   To incorporate your component into the flect Python project, add the following content to a `components.py` file:

   ```python
   from typing import Literal, Optional
   from flect import components as c


   class BaseUIComponent(c.Custom):
       package: Literal["docs-ui"] = "ui"
       sub_type: Literal["badge"] = "badge"


   class Badge(BaseUIComponent):
       class_name: Optional[str] = None
       text: str
   ```

7. **Using the Custom Component**

   Your custom component is now ready for use within the flect application, just like any built-in component. For example:

   ```python
   from flect import PageResponse
   from components import Badge

   async def page():
       return PageResponse(
           body=Badge(text="Hello Badge!"),
       )
   ```

   Upon starting the service, you'll be greeted with a badge displaying the message "Hello Badge!" on your webpage.

This guide provides a thorough walkthrough for integrating custom React components into the flect framework, thereby enhancing your web applications with greater flexibility and functionality.
