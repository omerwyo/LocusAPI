import logging
import json

from flask import request, jsonify

from LocusAPI import app

logger = logging.getLogger(__name__)

# basic public route, we ask for a tag -> retrieve from DB with related Tag, then return it.
@app.route('/v1/{tag}', methods=['GET'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    result = "Test"
    logging.info("My result :{}".format(result))
    return json.dumps(result)
