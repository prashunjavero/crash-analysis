import json

from flask import Flask
from src.util.logger import logger
from src.util.redis import Redis
from src.util.mongo import MongoClient
from src.util.config_parser import get_config
from src.api.user_api import user_bp
from src.api.file_api import file_bp

config = get_config()
roles_cache = Redis(host=config['redis']['host'], port=config['redis']['port'], db=config['redis']['roles_db'])

app = Flask(__name__)
PORT = 8000

# mongo db connection to connect to db
mongo = MongoClient(app).get_connection()
users = mongo.db.users

def seed_roles():
    """ method to seed roles """
    try:
        with open("../../roles.json", 'r') as stream:
            for role in json.load(stream)['roles']:
                # todo : validate the data before inserting
                roles_cache.set(role["name"],str(role["permissions"]),3600)
                logger.info('seeded role : {role}'.format(role= role["name"]))
    except RuntimeError as exc:
        logger.error('error seeding roles ')
        logger.error( str(exc))

def seed_users():
    """ method to seed roles """
    try:
        with open("../../users.json", 'r') as stream:
            for user in json.load(stream)['users']:
                # todo : validate the data before inserting
                users.insert_one(user)
                logger.info('seeded user : {user}'.format(user= user["name"]))
    except RuntimeError as exc:
        logger.error('error seeding users  ')
        logger.error( str(exc))

@app.route("/" , methods = ['GET'])
def getuser():
    ''' endpoints to get user information'''
    return  "howdy!"

if __name__ == '__main__':
    logger.info('starting application server ..')
    app.debug=True
    seed_roles()
    seed_users()
    app.register_blueprint(user_bp)
    app.register_blueprint(file_bp)
    app.run(host='0.0.0.0', port=PORT)
