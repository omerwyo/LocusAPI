import logging
import json
from flask import request, jsonify
from scraper import parseMOHFeed
from scraper import gov_sg_api_scrape

from LocusDev import app

logger = logging.getLogger(__name__)

@app.route('/v1/daily', methods=['GET'])
def dailyUpdates():
    numEntries = request.args.get('numEntries')
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = parseMOHFeed(numEntries)
    logging.info("My result :{}".format(result))
    return jsonify(result)

@app.route('/v1/govpress', methods=['GET'])
def generalData():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = gov_sg_api_scrape()
    logging.info("My result :{}".format(result))
    return jsonify(result)

