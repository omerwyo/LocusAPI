# import logging
# import json
# from flask import request, jsonify
# <<<<<<< scheduled-population
# from scraper import parseMOHFeed, gov_sg_api_scrape
# from models import Article
# from sqlalchemy import desc
# from App import app

# logger = logging.getLogger(__name__)

# # @app.route('/v1/daily', methods=['GET'])
# # def dailyUpdates():
# #     data = request.get_json()
# #     logging.info("data sent for evaluation {}".format(data))
# #     # result = parseMOHFeed()
# #     print("CHECK FOR PROBLEM")
# #     entities = Article.query.order_by(desc(Article.time)).all()
# #     print("ENTITIES")
# #     logging.info('RETURNING DB STUFF WORKS')
# #     # logging.info("My result :{}".format(result))
# #     return jsonify(json_list = entities)

# # @app.route('/v1/govpress', methods=['GET'])
# # def generalData():
# #     data = request.get_json()
# #     logging.info("data sent for evaluation {}".format(data))
# #     result = gov_sg_api_scrape()
# #     logging.info("My result :{}".format(result))
# #     return json.dumps(result)
# =======
# from scraper import parseMOHFeed
# from scraper import gov_sg_api_scrape

# from LocusDev import app

# logger = logging.getLogger(__name__)

# @app.route('/v1/daily', methods=['GET'])
# def dailyUpdates():
#     # numEntries = request.args.get('numEntries')
#     data = request.get_json()
#     logging.info("data sent for evaluation {}".format(data))
#     result = parseMOHFeed()
#     logging.info("My result :{}".format(result))
#     response = jsonify(result)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response

# @app.route('/v1/govpress', methods=['GET'])
# def generalData():
#     data = request.get_json()
#     logging.info("data sent for evaluation {}".format(data))
#     result = gov_sg_api_scrape()
#     logging.info("My result :{}".format(result))
#     response = jsonify(result)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response
# >>>>>>> master

