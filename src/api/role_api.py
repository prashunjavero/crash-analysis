# pylint: disable=import-error
# pylint: disable=fixme, no-else-return, no-member, line-too-long
''' endpoints for roles assignment and creation '''
from flask import Blueprint

roles_bp = Blueprint('roles', __name__)

@roles_bp.route("/roles/<name>" , methods = ['GET'])
def getrole(name):
    ''' endpoints to get roles information'''
    return  {}

@roles_bp.route("/role/<authenticated_user>" , methods = ['POST'])
def createrole(authenticated_user):
    ''' endpoints to create role '''
    return {}

@roles_bp.route("/role/update/<authenticated_user>" , methods = ['PUT'])
def updaterole(authenticated_user):
    ''' endpoints to update role'''
    return {}

@roles_bp.route("/user/<name>/<authenticated_user>" , methods = ['DELETE'])
def deleterole(name,authenticated_user):
    ''' endpoints to delete role'''
    return {}
