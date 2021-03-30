# pylint: disable=fixme, no-else-return, no-member ,import-error, line-too-long
''' validates the user based  on password and email from database'''
from flask import Flask,jsonify
from src.util.mongo import MongoClient
from src.util.logger import logger

app = Flask("abc")
mongo = MongoClient(app).get_connection()

class UserValidator:
    ''' constructor to validate user '''
    def __init__(self, user):
        self._user = user

    def validate(self, name):
        ''' validate user '''
        try:
            users = mongo.db.users
            db_user = users.find_one({"name":str(name)})
            if db_user is not None :
                if self._user.name == db_user["name"] and  self._user.password == db_user["password"] and self._user.email == db_user["email"] : # pylint: disable=simplifiable-if-statement
                    return True
                else:
                    return False
            else:
                return False
        except RuntimeError as err:
            logger.error(str(err))
            return jsonify({"status" : 500 , "message": str(err)}) , 500
