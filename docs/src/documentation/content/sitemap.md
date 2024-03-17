# Sitemap Integration in flect

Sitemaps play a crucial role in optimizing website visibility for search engines by providing a roadmap of all accessible paths within your application.

By default, flect automatically parses all the paths in your app to generate a sitemap. For dynamic routes, you have the flexibility to define a function within your page files that generates links for inclusion in the sitemap.

Here's how you can define a sitemap function for dynamic routes in Python:

```python
from flect.sitemap import Sitemap

async def sitemap(dynamic_url: str) -> list[Sitemap]:
    return [
        Sitemap(
            url=dynamic_url.format(slug_name=slug_name),
            last_modified=None,
            change_frequency=None,
            priority=None,
        )
        for slug_name in ["x", "y", "z"]
    ]
```

In this example, `slug_name` represents the variable portion of the dynamic route, and `["x", "y", "z"]` illustrates all possible values for `slug_name`. This approach allows you to easily include dynamic content in your sitemap, ensuring that search engines can discover and index these pages efficiently.
