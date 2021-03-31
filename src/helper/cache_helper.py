# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long, import-error, no-else-return
''' module create cache instances'''
from flask import jsonify
from src.util.config_parser import get_config
from src.util.redis import Redis
from src.util.logger import logger

#load the config from the yaml file
logger.info('loading configuration .... ')
config = get_config()
ACCESS_TOKEN_SECRET_KEY = config['jwt']['access_token']['access_token_secret']
REFRESH_TOKEN_SECRET_KEY = config['jwt']['refresh_token']['refresh_token_secret']
ACCESS_TOKEN_TTL = config['jwt']['access_token']['access_token_ttl']
REFRESH_TOKEN_TTL = config['jwt']['refresh_token']['refresh_token_ttl']

# connect to redis cache using the config
logger.info('connect to the token and claims cache  .... ')
token_cache = Redis(host=config['redis']['host'] , port=config['redis']['port'] , db = config['redis']['token_db'])
claims_cache = Redis(host=config['redis']['host'] , port=config['redis']['port'] , db = config['redis']['claims_db'])

def get_token_cache():
    ''' module to get token cache '''
    return token_cache

def get_claims_cache():
    ''' module to get claims cache '''
    return claims_cache

def set_token(user, access_token, refresh_token ):
    ''' set token in cache'''
    try:
        logger.info('setting access token and refresh tokens in the token cache ... ')
        # if the tokens do not exist save the tokens in cache
        if token_cache.exists("access_token_" + str(user.name)) == 0 and token_cache.exists("refresh_token_" + str(user.name)) == 0:
            token_cache.set("access_token_" + str(user.name),str({"access_token": access_token} ),ACCESS_TOKEN_TTL)
            token_cache.set("refresh_token_" + str(user.name),str({"refresh_token": refresh_token }),REFRESH_TOKEN_TTL)
        else:
        # if the tokens exist save and update the tokens in cache
            token_cache.delete("access_token_" + str(user.name))
            token_cache.delete("refresh_token_" + str(user.name))
            token_cache.set("access_token_" + str(user.name),str({"access_token": access_token} ),ACCESS_TOKEN_TTL)
            token_cache.set("refresh_token_" + str(user.name),str({"refresh_token": refresh_token }),REFRESH_TOKEN_TTL)
        return None
    except RuntimeError as err:
        logger.error(str(err))
        return jsonify({"status" : 500 , "message": str(err)}) , 500

def auth_response(access_token,refresh_token, name ):
    ''' create login response'''
    # generate the response if autentication is successfull
    try:
        if access_token is not None and refresh_token is not None:
            return_data = {
                "message": "Login Successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"
            }
            logger.info('generated tokens for user %s are : %s ' , name,return_data)
            return jsonify(return_data)
        else:
        # generate the HTTP 201 response if autentication is not successfull
            error = {'status' : 201 , 'message' : 'unauthorized user'}
            logger.error(' tokens can not be generated for user %s with response %s ' ,name,error)
            return jsonify(error) , 201
    except RuntimeError as err:
        logger.error(str(err))
        return jsonify({"status" : 500 , "message": str(err)}) , 500
