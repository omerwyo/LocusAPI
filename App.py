import logging
from flask import Flask, redirect, abort, request, jsonify
from flask_apscheduler import APScheduler
import time
from models import db
from sqlalchemy import desc
from models import Article
from scraper import parseMOHFeed, gov_sg_api_scrape, checkTags
from models import setup_db, db_drop_and_create_all
from flask_cors import CORS
import os
import datetime

scheduler = APScheduler()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

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

@scheduler.task("cron", id="wrapper", hour='15', minute='08')
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
    entities = Article.query.order_by(desc(Article.datePublished)).all()
    # entities = Article.query.all()
    print("ENTITIES")
    logging.info('RETURNING DB STUFF WORKS')
    # logging.info("My result :{}".format(result))
    response = jsonify(json_list=[e.serialize for e in entities])
    return response


# add some sort of authorisation, where the API key is needed for administrators to post up info
@app.route('/admin', methods=['POST'])
def adminNew():
    if not request.args.get('API_KEY') or request.args.get('API_KEY') != os.environ.get('LOCUS_API_KEY'): return jsonify({'message':'Please use a valid API Key!'}), 401
    data = request.get_json()
    newArticle = Article(articleId= data['articleLink'],
                         title=data['title'],
                         bodyText=data['bodyText'],
                         datePublished=datetime.datetime.now(),
                         description="")
    if data['articleLink']: newArticle.articleId = data['articleLink']
    # if data['articleDescription']: newArticle.description = data['articleDescription']

    db.session.add(newArticle)
    db.session.commit()

    logging.info("Data sent for evaluation {}".format(data))
    return jsonify({'message': 'Article Created successfully.'}), 200

@app.route('/admin', methods=['PUT'])
def adminPut():
    if not request.args.get('API_KEY') or request.args.get('API_KEY') != os.environ.get('LOCUS_API_KEY'): return jsonify({'message': 'Please use a valid API Key!'}), 401
    if not request.args.get('articleId'): return jsonify({'message': 'Please specify an articleId to update!'}), 400

    article = Article.query.filter_by(articleId=request.args.get('articleId').strip()).first()
    if not article: return jsonify({'message': 'No article found with specified ID.'}), 400

    data = request.get_json()
    article.title = data['title']
    article.bodyText = data['bodyText']
    article.articleId = data['articleLink']
    # article.datePublished = data['articleLink']
    # article.description = data['description']

    db.session.commit()
    return jsonify({'message': 'Article updated successfully.'}), 200

@app.route('/admin', methods=['DELETE'])
def adminDelete():
    if not request.args.get('API_KEY') or request.args.get('API_KEY') != os.environ.get('LOCUS_API_KEY'): return jsonify({'message': 'Please use a valid API Key!'}), 401
    if not request.args.get('articleId'): return jsonify({'message': 'Please specify an articleId to delete!'}), 400

    article = Article.query.filter_by(articleId=request.args.get('articleId').strip()).first()
    db.session.delete(article)
    db.session.commit()

    return jsonify({'message': 'Article deleted successfully.'}), 200

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
