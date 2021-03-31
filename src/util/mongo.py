# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long, import-error, too-few-public-methods)
""" Mongo client class. to handle mongo connection"""
from flask import jsonify
from flask_pymongo import PyMongo
from src.util.logger import logger
from src.util.config_parser import get_config

config = get_config()
class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args)
        return cls._instance

class MongoClient(metaclass=Singleton):
    """
    Mongo client class.
    """
    def __init__(self,app):
        self.app = app

    def get_connection(self):
        """
         return mongo connection
        """
        try:
            logger.info('connecting to mogodb.. ')
            # todo: remove the hard coding
            self.app.config['MONGO_DBNAME'] = config['mongo']['default_db']
            self.app.config["MONGO_URI"] = config['mongo']['mongo_uri']
            mongo = PyMongo(self.app)
            return mongo
        except ConnectionError as err:
            logger.error(str(err))
            return jsonify({"status" : 500 , "message": str(err)}) , 500
