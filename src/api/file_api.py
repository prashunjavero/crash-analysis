# pylint: disable=import-error
# pylint: disable=fixme, no-else-return, no-member, line-too-long
''' endpoints for file download '''
from flask import Blueprint,request,jsonify
from src.util.logger import logger
from src.helper.user_helper import has_access
from src.services.file_service import download_and_save
file_bp = Blueprint('file', __name__)

@file_bp.route("/file/download/<authenticated_user>" , methods = ['POST'])
def download(authenticated_user):
    ''' endpoints to download file '''
    if has_access(request, authenticated_user):
        logger.info('getting and saving data form endpoint %s', request.json["endpoint"])
        return download_and_save(request)
    return jsonify({'status' : 201 , 'message' : 'unauthorized user'}) ,201
