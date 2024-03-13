# Custom Component

Custom components allow you to use your own developed React components within Flect. In this guide, we'll walk through the process of creating a simple badge component.

## Steps

1. **Install the Custom Component Template Project**

   Begin by navigating to the root directory of your flect project. Execute the following commands to clone the custom component template project from the [cookiecutter repository](https://github.com/Chaoyingz/cookiecutter-flect-custom-component) and set up your development environment:

   ```console
   cookiecutter https://github.com/Chaoyingz/cookiecutter-flect-custom-component
   cd {package_name}
   pnpm install
   ```

   This template is based on Vite [react-ts](https://vite.new/react-ts) and comes with TailwindCSS pre-installed.

2. **Create Your React Custom Component**

   The project starts with a button component example, which you can remove. Next, create a new custom component file named `badge.tsx` in the `lib/components` directory. Here's an example:

   ```tsx
   interface BadgeProps {
     text: string
   }

   export const Badge = (props: BadgeProps) => {
     return (
       <div className="inline-flex rounded-md px-2.5 py-0.5 text-xs font-semibold bg-primary text-primary-foreground">
         {props.text}
       </div>
     )
   }
   ```

   This component accepts a `text` field for display. Import this component in `lib/index.ts`:

   ```tsx
   import './index.css'

   import { Badge } from './components/badge.tsx'

   export { Badge }
   ```

   Use the `pnpm run build` command to compile your work into a custom component library.

3. **Register the Custom Component in Python**

   Once your custom component is ready, define the corresponding Pydantic class in Python.

   ```python
   from flect.components import Custom
   from typing import Literal

   class Badge(Custom):
       package: str = "docs-ui"
       component: Literal["Badge"] = "Badge"
       text: str

   ```

   The `package` field should match the name of the package you created for your React custom component, and `component` should match the component name. The remaining fields represent the component's props.

4. **Use the Custom Component**

   You can now use this component as shown below:

   ```python
   from flect import PageResponse
   from flect import components as c

   from .components import Badge

   async def page() -> PageResponse:
       return PageResponse(
           body=c.Container(
               children=[Badge(text="custom badge")]
           ),
       )
   ```

   After executing the above, you should see a badge component displayed.
   ![custom-badge](https://github.com/Chaoyingz/flect/assets/32626585/70e9dab0-772c-4c04-b6e6-6a460fc1054b)

## Conclusion

That’s it! You have successfully created and used a custom component in flect. This process allows you to extend the capabilities of Flect by using your own React components. Remember, the key to creating effective custom components is understanding the specific needs of your project. Happy coding!
