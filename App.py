import logging
from flask import Flask, redirect, abort, request, jsonify
from flask_apscheduler import APScheduler
import time
# from models import db
from sqlalchemy import desc
from models import Article
from scraper import parseMOHFeed, gov_sg_api_scrape, checkTags
from models import setup_db, db_drop_and_create_all

scheduler = APScheduler()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """ uncomment at the first time running the app """
    # db_drop_and_create_all()

    # @app.errorhandler(500)
    # def server_error(error):
    #     return jsonify({
    #         "success": False,
    #         "error": 500,
    #         "message": "server error"
    #     }), 500

    return app

app = create_app()

@scheduler.task("cron", id="wrapper", hour='11', minute='07')
def wrapperTask():
    parseMOHFeed()
    time.sleep(5)
    gov_sg_api_scrape()
    time.sleep(5)
    checkTags()
    time.sleep(2)
    return

@app.route('/v1/daily', methods=['GET'])
def dailyUpdates():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    # result = parseMOHFeed()
    print("CHECK FOR PROBLEM")
    # entities = Article.query.order_by(desc(Article.datePublished)).all()
    entities = Article.query.all()
    print("ENTITIES")
    logging.info('RETURNING DB STUFF WORKS')
    # logging.info("My result :{}".format(result))
    return jsonify(json_list = entities)

@app.route('/', methods=['GET'])
def default_route():
    # the homepage redirects to our API Developer Documentation page
    return redirect("https://dev.locus.social/")

logger = logging.getLogger(__name__)
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":

    # our scheduler function goes here:
    scheduler.start()
    logging.info("Starting application ...")
    app.run(debug=False, port=33507)
