from typing import TYPE_CHECKING, Literal, Optional
from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element, SubElement, tostring

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from tui.routing import ClientRoute


class Sitemap(BaseModel):
    url: str
    last_modified: Optional[str]
    change_frequency: Optional[Literal["always", "hourly", "daily", "weekly", "monthly", "yearly", "never"]]
    priority: Optional[float] = Field(None, ge=0.0, le=1.0)


async def get_sitemap_objs(routes: list["ClientRoute"]) -> list[Sitemap]:
    sitemaps = []
    for route in routes:
        if route.is_page:
            if route.sitemap:
                sitemaps.extend(await route.sitemap(route.url))
            elif not route.is_dynamic:
                sitemaps.append(Sitemap(url=route.url, last_modified=None, change_frequency=None, priority=None))
        sitemaps.extend(await get_sitemap_objs(route.children))
    return sorted(sitemaps, key=lambda sitemap: sitemap.url)


async def generate_sitemap_xml(
    routes: list["ClientRoute"],
    base_url: str,
) -> str:
    sitemap_objs = await get_sitemap_objs(routes)
    sitemap = Element("urlset")
    sitemap.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    for sitemap_obj in sitemap_objs:
        url_element = SubElement(sitemap, "url")

        loc = SubElement(url_element, "loc")
        loc.text = f"{base_url}{sitemap_obj.url}"

        if sitemap_obj.last_modified:
            lastmod = SubElement(url_element, "lastmod")
            lastmod.text = sitemap_obj.last_modified

        if sitemap_obj.change_frequency:
            change_freq = SubElement(url_element, "changefreq")
            change_freq.text = sitemap_obj.change_frequency

        if sitemap_obj.priority is not None:
            priority = SubElement(url_element, "priority")
            priority.text = str(sitemap_obj.priority)

    return parseString(tostring(sitemap, encoding="utf-8")).toprettyxml()
