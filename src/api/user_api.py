# pylint: disable=import-error
# pylint: disable=fixme, no-else-return, no-member, line-too-long
''' endpoints for user authentication'''
from flask import Blueprint
from src.services.user_service import login,get_user,create_user,update_user,delete_user

user_bp = Blueprint('user', __name__)

@user_bp.route("/login" , methods = ['POST'])
def _login():
    ''' endpoints to authenticate users'''
    return login()

@user_bp.route("/user/<name>" , methods = ['GET'])
def _get_user(name):
    ''' endpoints to get user information'''
    return  get_user(name)

@user_bp.route("/user/<authenticated_user>" , methods = ['POST'])
def _create_user(authenticated_user):
    ''' endpoints to create user '''
    return create_user(authenticated_user)

@user_bp.route("/user/<authenticated_user>" , methods = ['PUT'])
def _update_user(authenticated_user):
    ''' endpoints to update user'''
    return update_user(authenticated_user)

@user_bp.route("/user/<name>/<authenticated_user>" , methods = ['DELETE'])
def _deleteuser(name,authenticated_user):
    ''' endpoints to delete user'''
    return  delete_user(name,authenticated_user)
