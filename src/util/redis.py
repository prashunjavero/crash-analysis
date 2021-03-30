# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long, import-error
''' module to interact with redis'''
import redis
from flask import jsonify
from src.util.logger import logger
class Redis:
    ''' create redis connection'''
    def __init__(self, host='redis' , port=6379 , db = 0):
        self.rcache = redis.Redis(host=host, port=port, db=db)

    def set(self, key, value ,ttl):
        '''set key value pair to redis with ttl '''
        try:
            self.rcache.set(key, value, ttl)
            return None
        except RuntimeError as err:
            logger.error(str(err))
            return jsonify({"status" : 500 , "message": str(err)}) , 500

    def get(self, key ):
        ''' get key value pair from redis '''
        try:
            result = None
            if self.exists(key):
                result = self.rcache.get(key).decode("utf-8")
            else:
                logger.error('error getting value for key %s from redis' , key )
            return result
        except RuntimeError as err:
            logger.error(str(err))
            return jsonify({"status" : 500 , "message": str(err)}) , 500


    def exists( self, key ):
        ''' check if key exists in redis '''
        try:
            return self.rcache.exists(key)
        except RuntimeError as err:
            logger.error(str(err))
            return jsonify({"status" : 500 , "message": str(err)}) , 500

    def delete( self, key ):
        ''' delete if key exists in redis '''
        try:
            if self.exists(key):
                self.rcache.delete(key)
            return key
        except RuntimeError as err:
            logger.error(str(err))
            return jsonify({"status" : 500 , "message": str(err)}) , 500
