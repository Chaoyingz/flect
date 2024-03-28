import re

from flect.constants import GROUP_ROUTE_PREFIX, LAYOUT_ROUTE_SUFFIX


def path_priority(path: str) -> tuple:
    """
    Calculate the priority of a route path based on several weighted factors.

    Parameters:
    - path (str): The route path for which to calculate the priority.

    Returns:
    - tuple: A tuple representing the path's priority. Lower values indicate higher priority. The factors are:
        1. catch_all_weight: Infinity if the path includes a catch-all pattern, indicating it should be matched last. Otherwise, 0.
        2. depth_weight: The depth of the path, with deeper paths considered more specific and thus lower priority.
        3. segment_weight: The last valid segment of the path, used for sorting when depths are equal.
        4. layout_weight: 1 if the path is for a layout route, 0 otherwise. Layout routes typically have lower priority.
        5. dynamic_weight: 1 if the path is for a dynamic route, 0 otherwise. Dynamic routes typically have lower priority.
    """

    # Normalize path for processing
    normalized_path = re.sub(rf"{GROUP_ROUTE_PREFIX}[^/]+/", "", path)
    if normalized_path.endswith(LAYOUT_ROUTE_SUFFIX):
        normalized_path = normalized_path[: -len(LAYOUT_ROUTE_SUFFIX)]

    parts = normalized_path.strip("/").split("/")

    # Calculate weights
    catch_all_weight = float("inf") if "{path:path}" in normalized_path else 0
    depth_weight = len(parts)
    segment_weight = parts[-1] if parts else ""
    layout_weight = 1 if path.endswith(LAYOUT_ROUTE_SUFFIX) else 0
    dynamic_weight = 1 if path.endswith("}/") else 0

    return catch_all_weight, depth_weight, segment_weight, layout_weight, dynamic_weight
