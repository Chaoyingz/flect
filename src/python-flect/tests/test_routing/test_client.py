import pytest
from flect.constants import ROOT_ROUTE_PREFIX
from flect.routing.client import RouteInfo, get_client_routes, parse_route_info_from_folder

from tests.conftest import APP_FOLDER


@pytest.mark.parametrize(
    "folder,is_root_folder,parent_path,absolute_path,expected",
    [
        (
            APP_FOLDER,
            True,
            "/",
            "/",
            RouteInfo("", "/", "/", "/flect/"),
        ),
        (
            APP_FOLDER / "segment1",
            False,
            "/",
            "/",
            RouteInfo("segment1", "/segment1/", "/segment1/", f"{ROOT_ROUTE_PREFIX}/segment1/"),
        ),
        (
            APP_FOLDER / "segment1" / "dynamic__segment_id",
            False,
            "/",
            "/",
            RouteInfo(
                "{segment_id}", "/{segment_id}/", "/dynamic__segment_id/", f"{ROOT_ROUTE_PREFIX}/{{segment_id}}/"
            ),
        ),
        (
            APP_FOLDER / "segment1" / "group__segment2",
            False,
            "/",
            "/",
            RouteInfo("", "/", "/group__segment2/", f"{ROOT_ROUTE_PREFIX}/group__segment2/"),
        ),
        (
            APP_FOLDER / "segment1" / "group__segment2" / "segment3",
            False,
            "/segment1/",
            "/segment1/group__segment2/",
            RouteInfo(
                "segment3",
                "/segment1/segment3/",
                "/segment1/group__segment2/segment3/",
                f"{ROOT_ROUTE_PREFIX}/segment1/segment3/",
            ),
        ),
    ],
)
def test_parse_route_info_from_folder(
    folder,
    is_root_folder,
    parent_path,
    absolute_path,
    expected,
):
    route = parse_route_info_from_folder(folder, is_root_folder, parent_path, absolute_path)
    assert route == expected


def test_get_client_routes(app_folder):
    routes = get_client_routes(app_folder)
    assert [route.model_dump() for route in routes] == [
        {
            "segment": "",
            "path": "/",
            "absolute_path": "/flect/",
            "loader_path": "/flect/_layout/",
            "index": False,
            "children": [
                {
                    "segment": "segment1",
                    "path": "/segment1/",
                    "absolute_path": "/flect/segment1/",
                    "loader_path": "/flect/segment1/_layout/",
                    "index": False,
                    "children": [
                        {
                            "segment": "",
                            "path": "/segment1/",
                            "absolute_path": "/flect/segment1/group__segment2/",
                            "loader_path": "/flect/segment1/group__segment2/_layout/",
                            "index": False,
                            "children": [
                                {
                                    "segment": "segment3",
                                    "path": "/segment1/segment3/",
                                    "absolute_path": "/flect/segment1/group__segment2/segment3/",
                                    "loader_path": "/flect/segment1/segment3/",
                                    "index": False,
                                    "children": [],
                                }
                            ],
                        },
                        {
                            "segment": "{segment_id}",
                            "path": "/segment1/{segment_id}/",
                            "absolute_path": "/flect/segment1/dynamic__segment_id/",
                            "loader_path": "/flect/segment1/{segment_id}/",
                            "index": False,
                            "children": [],
                        },
                        {
                            "segment": "segment2",
                            "path": "/segment1/segment2/",
                            "absolute_path": "/flect/segment1/segment2/",
                            "loader_path": "/flect/segment1/segment2/",
                            "index": False,
                            "children": [],
                        },
                        {
                            "segment": "segment1",
                            "path": "/segment1/",
                            "absolute_path": "/flect/segment1/",
                            "loader_path": "/flect/segment1/",
                            "index": True,
                            "children": [],
                        },
                    ],
                },
                {
                    "segment": "",
                    "path": "/",
                    "absolute_path": "/flect/",
                    "loader_path": "/flect/",
                    "index": True,
                    "children": [],
                },
            ],
        }
    ]
