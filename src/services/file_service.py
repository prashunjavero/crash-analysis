""" file handler service """
# pylint: disable=import-error
# pylint: disable=fixme, no-else-return, no-member, line-too-long
from flask import request,jsonify
from src.util.logger import logger
from src.helper.user_helper import has_access
from src.helper.file_helper import download_and_save

def download_file(authenticated_user):
    """ 
    if the user is uthenticated and had the authorization download the file 
    from the posted endpoint
    """
    if has_access(request, authenticated_user):
        logger.info('getting and saving data form endpoint %s', request.json["endpoint"])
        return download_and_save(request)
    return jsonify({'status' : 201 , 'message' : 'unauthorized user'}) ,201
