import os
import yaml


def get_model(model):
    model_file = os.path.join('.korapp', f'model_{model}.yaml')
    with open(model_file, 'r') as stream:
        result = yaml.load(stream, Loader=yaml.FullLoader)
    return result
