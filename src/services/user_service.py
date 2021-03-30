""" service to handle user CRUD operations"""
from datetime import datetime, timedelta
import ast
import jwt

from flask import Flask,request, jsonify

from src.entities.user import User
from src.util.logger import logger
from src.util.validate_user import UserValidator
from src.helper.cache_helper import set_token,auth_response
from src.helper.cache_helper import ACCESS_TOKEN_SECRET_KEY,REFRESH_TOKEN_SECRET_KEY,ACCESS_TOKEN_TTL
from src.helper.user_helper import find_user, create_new_user, is_valid_token, has_valid_claims, delete_existing_user, update_existing_user
from src.util.mongo import MongoClient
from src.util.redis import Redis

app = Flask(__name__)

# mongo db connection to connect to db
mongo = MongoClient(app).get_connection()

#todo:remove the hard coding
roles_cache = Redis(host='redis', port=6379, db=0)

def login():
    """ returns the JWT token if the login is successfull """
    body  = request.json
    logger.info('logging in user %s with body %s' ,body['name'], body )
    # create user
    user = User(body['name'],body['password'],body['email'],body["roles"])
    # check if the user is valid
    is_valid_user = UserValidator(user).validate(body['name'])
    time_limit = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_TTL)
    payload = {"user_name": user.name ,"exp":time_limit, "scope": user.roles }
    if is_valid_user:
        logger.info('generating access and refresh tokens for user %s' , user.name)
        # if the user is valid generate access token and refresh token
        access_token = jwt.encode(payload,ACCESS_TOKEN_SECRET_KEY)
        refresh_token = jwt.encode(payload,REFRESH_TOKEN_SECRET_KEY)
        set_token(user,access_token,refresh_token)
        return auth_response(access_token,refresh_token,body['name']) , 200
    else:
        logger.error('authentication failed for user %s' , user.name)
        # return HTTP status 201 for un authorized user
        return jsonify({'status' : 201 , 'message' : 'unauthorized user'}) ,201

def get_user(name):
    """ gets the user with the given name """
    # get the base url from the request
    request_url = "/"+ str(request.url.split("/")[3])
    # check if token is valid
    if is_valid_token(request,name):
        return find_user(name)
    return jsonify({'status' : 201 , 'message' : 'unauthorized user'}) ,201

def update_user(authenticated_user):
    """ updates the user if the current user(authenticated user) has permissions """
    body  = request.json
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
                    logger.info('updating user %s for user %s' ,body, authenticated_user)
                    return update_existing_user(body)
                    break;
    return jsonify({'status' : 201 , 'message' : 'unauthorized user'}) ,201


def create_user(authenticated_user):
    """ creates the user if the current user(authenticated user) has permissions """
    body  = request.json
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
                    logger.info('creating user %s for user %s' ,body, authenticated_user)
                    return create_new_user(body)
                    break;
    return jsonify({'status' : 201 , 'message' : 'unauthorized user'}) ,201


def delete_user(name,authenticated_user):
    """ deletes the user if the current user(authenticated user) has permissions """
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
                    logger.info('deleting user %s for user %s' ,name, authenticated_user)
                    return delete_existing_user(name)
                    break;
    return jsonify({'status' : 201 , 'message' : 'unauthorized user'}) ,201