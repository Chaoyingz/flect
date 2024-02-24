from tui.sitemap import generate_sitemap_xml, get_sitemap_objs


async def test_get_sitemap_objs(client_routes):
    sitemaps = await get_sitemap_objs(client_routes)
    assert sitemaps


async def test_generate_sitemap_xml(client_routes):
    sitemap = await generate_sitemap_xml(
        client_routes,
        "http://localhost:8000",
    )
    assert sitemap
