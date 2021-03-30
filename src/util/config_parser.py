# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long, import-error
''' module parse the config yaml'''
import yaml
from flask import jsonify
from src.util.logger import logger

def get_config():
    ''' module returns the config as json '''
    with open("../../config/env.yml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as err:
            logger.error(str(err))
            return jsonify({"status" : 500 , "message": str(err)}) , 500