from datetime import datetime


def str_to_datetime(string: str)-> datetime:
    """Transforms string like '2020-05-07T01:00:00Z' to struct_time

    Args:
        string (str): string to transform

    Returns:
        struct_time: datetime
    """
    return datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ')