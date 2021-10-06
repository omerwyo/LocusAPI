import json
import logging
from flask import request

from LocusAPI import app

logger = logging.getLogger(__name__)

# add some sort of authorisation, where the API key is needed for administrators to post up info
@app.route('/admin', methods=['POST'])
def admin():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    result = ""
    logging.info("My result :{}".format(result))
    return json.dumps(result)


