# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long, import-error, no-else-return
""" file service to handle files """
import time
from io import StringIO
import requests
import pandas as pd
from flask import Flask,jsonify
from src.util.logger import logger
from src.util.mongo import MongoClient

app = Flask(__name__)

# mongo db connection to connect to db
mongo = MongoClient(app).get_connection()

def download_and_save(request):
    """ get ddata from posted endpont stream it and thesn save it to the db"""
    try:
        response  = requests.get(request.json["endpoint"])
        data_frame = pd.read_csv(StringIO(response.content.decode('utf-8')))
        if data_frame.empty:
            return jsonify({"status" : 500 , "message": "no response returned from endpoint "}) , 500
        df_converted_to_dict = data_frame.to_dict(orient='records')
        vehicle_crashes = mongo.db.crash
        for row in df_converted_to_dict:
            logger.info(' insering row %s', str(row))
            # should publish to kafka and insert should be handled by kafka consumer
            vehicle_crashes.insert(row)
            time.sleep(1)
        return jsonify({"status" : 200 , "message": "records inserted successfully"}) , 200
    except RuntimeError as err:
        logger.error(str(err))
        return jsonify({"status" : 500 , "message": str(err)}) , 500
