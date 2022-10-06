def url_to_username(string: str)-> str:
    """Transforms string like '/profesores/davinci137/' to username
    
    Args:
        string (str): string to transform
    
    Returns:
        str: username
    """
    return string.split('/')[-2]
