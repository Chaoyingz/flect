import re

from flect.constants import DYNAMIC_ROUTE_PREFIX


def path_priority(path: str) -> tuple:
    path = re.sub(rf"{DYNAMIC_ROUTE_PREFIX}[^/]+/", "", path)
    parts = path.split("/")

    catch_all_weight = float("inf") if "{path:path}" in path else 0
    depth_weight = len(parts)
    dynamic_weight = int(path.count("{"))
    segment_weight = parts[-2] if len(parts) >= 2 else ""
    return catch_all_weight, depth_weight, segment_weight, dynamic_weight
