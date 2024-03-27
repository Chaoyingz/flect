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
    assert routes
