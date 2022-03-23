from typing import Optional, Union, List
from json import loads as json_loads
from logging import getLogger

logger = getLogger('log_print')


def resolve(attr_map: dict, hash: dict) -> Union[str, int, dict, list]:
    """Get a PRELOAD_STATE and clean it with attr_map. 

    Args:
        attr_map (dict): Hash with attributes as {'multiple': true|false, 'attibutes': {...}, 'path': '...'}
        hash (dict): PRELOAD_STATE or some part of it

    Returns:
        Union[str, int, dict, list]: Hash|List with attributes or just an attribute
    """
    raw_base = get_value_from_path(attr_map['path'], hash)
    fill_method = get_value_list if attr_map['multiple'] else get_single_value

    return fill_method(raw_base, attr_map.get('attributes'))


def get_preload_state(html: str) -> dict:
    """Search line in html that describe window.__PRELOADED_STATE__ and
    return its content as dictionary.

    Args:
        html (str): HTML content decoded

    Returns:
        dict: page's PRELOAD_STATE 
    """
    for line in html.split('\n'):
        if 'window.__PRELOADED_STATE__' not in line:
            continue

        start = line.index('{')
        json_str = line[start:].replace('</script>', '')

        return json_loads(json_str)

    logger.error("Can't extract __PRELOADED_STATE__ from html.")
    return {}


def _csv_to_path(_csv: str) -> list:
    """Convert csv string to list of keys.

    >>> _csv_to_path('a,b,c')
    ['a', 'b', 'c']

    Args:
        _csv (str): csv string

    Returns:
        list: list of keys
    """
    return _csv.split(',')


def _go_to_path(path: list, hash: dict) -> Union[str, int, dict, list]:
    """Go to path in hash and return value.

    Args:
        path (list): list of keys
        hash (dict): hash to go to

    Returns:
        Union[str, int, dict, list]: value of key in hash
    """
    response = hash
    for key in path:
        response = response[key]
    return response


def get_value_from_path(path: str, hash: dict) -> Union[str, int, dict, list]:
    """Get value from path in hash.

    Args:
        path (str): path to value as csv string
        hash (dict): hash to go to

    Returns:
        Union[str, int, dict, list]: value of key in hash
    """
    return _go_to_path(_csv_to_path(path), hash)


def get_single_value(raw_base: Union[str, int, dict], attr_map: Optional[dict]) -> Union[str, int, dict]:
    """Build attribute from raw_base and attr_map.

    Args:
        raw_base (Union[str, int, dict]): A hash that could have trash in it
        attr_map (Optional[dict]): Hash with attributes as {'attr_1': {}, 'attr_2': {}, ...}

    Returns:
        Union[str, int, dict]: A hash with attributes or just attribute
    """
    if not attr_map:
        return raw_base
    return {key: resolve(value, raw_base) for key, value in attr_map.items()}


def get_value_list(raw_base: list, attr_map: dict) -> List[Union[str, int, dict]]:
    """Build List of attributes from raw_base and attr_map.

    Args:
        raw_base (list): A list of hashes that could have trash in it
        attr_map (dict): Hash with attributes as {'attr_1': {}, 'attr_2': {}, ...}

    Returns:
        list[Union[str, int, dict]]: List of attributes
    """
    return [get_single_value(row, attr_map) for row in raw_base]
