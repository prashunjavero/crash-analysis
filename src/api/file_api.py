# pylint: disable=import-error
# pylint: disable=fixme, no-else-return, no-member, line-too-long
''' endpoints for file download '''
from flask import Blueprint
from src.services.file_service import download_file

file_bp = Blueprint('file', __name__)

@file_bp.route("/file/download/<authenticated_user>" , methods = ['POST'])
def download(authenticated_user):
    ''' endpoints to download file '''
    return download_file(authenticated_user)
