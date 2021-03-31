# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long, import-error,no-else-return
""" helper functions for user service """
import ast
from flask import Flask,jsonify
from src.util.mongo import MongoClient
from src.helper.cache_helper import get_token_cache
from src.util.logger import logger
from src.util.config_parser import get_config
from src.util.redis import Redis

app = Flask(__name__)
mongo = MongoClient(app).get_connection()

config = get_config()

token_cache = get_token_cache()
roles_cache = Redis(host=config['redis']['host'], port=config['redis']['port'], db=config['redis']['roles_db'])

def verify_token(token):
    """ verify the token is not none"""
    # verifying that the token is not none
    logger.info('verifying the token ..')
    if token is None:
        return jsonify({'status' : 201, 'message' : 'user not authorized to call endpoint '}), 201
    else:
        return token

def is_valid_token(req,name):
    """ checks if the token is valid """
    # checks the token passed in the header is equal to the cached token
    try:
        bearer_token = req.headers.get('Authorization')
        auth_token  = bearer_token.split(" ")[1]
        cached_token = verify_token(token_cache.get("access_token_" + str(name)))
        token_json = ast.literal_eval(cached_token)
        token = verify_token(token_json)
        return bool(token is not None and token_json['access_token'] == auth_token)
    except RuntimeError as err:
        logger.error(str(err))
        return jsonify({"status" : 500 , "message": str(err)}) , 500

def has_valid_claims(claim,request_url,method):
    """ checks if the user has valid claims  """
    # checks that the user has claim to access the api
    return bool(claim['baseUrl'] == request_url and claim['method'].index(method) != -1 )

def create_new_user(user):
    """ creates the user """
    try:
        users = mongo.db.users
        users.insert_one(user)
        logger.info('inserted user %s in db' , user)
        db_user = users.find_one({"name":str(user["name"])})
        if db_user["name"] is not None :
            return jsonify({"status" : 200 , "message": "user created"}) , 200
        else:
            logger.info('failed to insert user %s in db' , user)
            return jsonify({'status' : 500 , 'message' : 'user not created'}) , 500
    except RuntimeError as err:
        logger.error(str(err))
        return jsonify({"status" : 500 , "message": str(err)}) , 500

def update_existing_user(user):
    """ creates the user """
    try:
        users = mongo.db.users
        users.update_one({"name":str(user["name"])},{"$set": user }, upsert=True)
        logger.info('updated user %s in db' , user)
        db_user = users.find_one({"name":str(user["name"])})
        if db_user["name"] is not None :
            return jsonify({"status" : 200 , "message": "user updated"})
        else:
            logger.info('failed to insert user %s in db' , user)
            return jsonify({'status' : 500 , 'message' : 'user not updated'}) , 500
    except RuntimeError as err:
        logger.error(str(err))
        return jsonify({"status" : 500 , "message": str(err)}) , 500

def find_user(name):
    """ finds the user """
    try:
        users = mongo.db.users
        db_user = users.find_one({"name":str(name)})
        logger.info('found user %s in db for user with name %s' ,db_user,name)
        if db_user is not None:
            return {
                "user" : {
                    "email": db_user["email"],
                    "username":db_user["name"],
                    "passowrd":db_user["password"],
                    "address" : db_user["address"]
                }
            }
        else:
            logger.error('error returning user for user with name %s' , name )
            return jsonify({'status' : 404 , 'message' : 'no user found'}) , 404
    except RuntimeError as err:
        logger.error(str(err))
        return jsonify({"status" : 500 , "message": str(err)}) , 500

def delete_existing_user(name):
    """ delete user with given name """
    try:
        users = mongo.db.users
        #delete sdocument
        users.delete_many({"name":str(name)})
        logger.info('deleting user with name %s',name)
        db_user = users.find_one({"name":str(name)})
        logger.info(db_user)
        if db_user is None :
            logger.error('deleted user with name %s', name)
            return jsonify({"status" : 200 , "message": "user  deleted"}) , 200
        else :
            logger.info('can not delete user with name %s', name)
            return jsonify({"status" : 200 , "message": "user not deleted"}) , 500
    except RuntimeError as err:
        logger.error(str(err))
        return jsonify({"status" : 500 , "message": str(err)}) , 500

def has_access(request,authenticated_user):
    """ checks if the use has access """
    # get the base url from the request
    request_url = "/"+ str(request.url.split("/")[3])
    # get the claims from the user
    users = mongo.db.users
    user = users.find_one({'name':str(authenticated_user)})
    if user is None:
        return jsonify({'status' : 404 , 'message' : 'no user found'}) , 404
    roles = user["roles"]
    if user is not None and is_valid_token(request,authenticated_user):
        for role in roles:
        # get the role from the roles cache
            permissions = ast.literal_eval(roles_cache.get(role))
            for permission in permissions:
                if has_valid_claims(permission,request_url,request.method):
                    return True
            break
    return False
