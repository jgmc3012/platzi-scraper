import yaml 


def get_yaml(path:str)->dict:
    with open(path, 'r') as stream:
        response = yaml.safe_load(stream)
    return response
