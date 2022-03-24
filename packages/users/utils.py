import re


def get_username_from_profile_path(path_profile:str):
    """
    Transform "/p/bmazariegos/" to "bmazariegos"
    """
    return path_profile[3:-1]

def get_username_from_avatar(avatar_url:str):
    """
    Transform "https://static.platzi.com/media/avatars/alan-isaac_vazquez_807714c1-eccc-4a11-8fd2-780569392832" to "alan-isaac_vazquez"
    """
    match = re.search(r'avatars/(.*)_.*', avatar_url)
    if match:
        return match.group(1)

    raise ValueError(f"Cant get username from avatar url: {avatar_url}")