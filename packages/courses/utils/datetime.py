from time import strptime, struct_time


def str_to_datetime(string: str)-> struct_time:
    """Transforms string like '2020-05-07T01:00:00Z' to struct_time

    Args:
        string (str): string to transform

    Returns:
        struct_time: datetime
    """
    return strptime(string, '%Y-%m-%dT%H:%M:%SZ')