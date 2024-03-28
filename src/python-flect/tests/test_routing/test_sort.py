from flect.routing.sort import path_priority


def test_sort_path():
    paths = [
        "/flect/_layout/",
        "/flect/segment1/_layout/",
        "/flect/segment1/segment3/",
        "/flect/segment1/{segment_id}/",
        "/flect/segment1/segment2/",
        "/flect/segment1/",
        "/flect/",
        "{path:path}",
        "/flect/segment1/group__segment_id/",
    ]

    assert sorted(paths, key=path_priority) == [
        "/flect/",
        "/flect/_layout/",
        "/flect/segment1/",
        "/flect/segment1/group__segment_id/",
        "/flect/segment1/_layout/",
        "/flect/segment1/segment2/",
        "/flect/segment1/segment3/",
        "/flect/segment1/{segment_id}/",
        "{path:path}",
    ]
