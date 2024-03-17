# TailwindCSS in flect

flect enables the use of [TailwindCSS](https://tailwindcss.com/) within Python to define styles. This integration is facilitated through TailwindCSS's [safelist](https://tailwindcss.com/docs/content-configuration#safelisting-classes) feature, allowing you to utilize a variety of TailwindCSS class names directly in Python.

Below is a list of TailwindCSS class names you can use in Python, supported by the safelist configuration:

```js
safelist: [
  'sr-only',
  {
    pattern: /^(w|max-w|h|max-h)-/,
  },
  {
    pattern: /^(flex|grid)-/,
  },
  {
    pattern: /^(m|p)\w?-\d/,
  },
  {
    pattern: /^gap-\d/,
  },
  {
    pattern: /^text-(\w{2}|\d{1}\w{2})$/,
  },
  {
    pattern: /^(font|justify)-/,
  },
  'border-b',
  'text-center',
  'invisible',
  'absolute',
  'overflow-hidden',
  'underline',
  'min-h-screen',
]
```

This configuration covers a wide range of utility classes for spacing, sizing, typography, flexbox, grid, visibility, positioning, overflow control, text decoration, and more. Additionally, you have the option to modify or extend this list through custom component definitions, providing a flexible way to tailor TailwindCSS styling within your flect applications.
