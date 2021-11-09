import datetime
import json
import logging
from flask import request, jsonify
import os
from scraper import Article
from models import db

logger = logging.getLogger(__name__)

# add some sort of authorisation, where the API key is needed for administrators to post up info
@app.route('/admin', methods=['POST'])
def adminNew():
    if not request.args.get('API_KEY') or request.args.get('API_KEY') != os.environ.get('LOCUS_API_KEY'): return jsonify({'message':'Please use a valid API Key!'}), 401
    data = request.get_json()
    newArticle = Article(articleId= data['articleLink'],
                         title=data['articleLink'],
                         bodyText=data['articleLink'],
                         datePublished=data['articleLink'],
                         description="")
    if data['articleLink']: newArticle.articleId = data['articleLink']
    if data['articleDescription']: newArticle.description = data['articleDescription']

    db.session.add(newArticle)
    db.session.commit()

    logging.info("Data sent for evaluation {}".format(data))
    result = ""
    logging.info("My result :{}".format(result))
    return json.dumps(result)

@app.route('/admin/update', methods=['PUT'])
def adminPut():
    if not request.args.get('API_KEY') or request.args.get('API_KEY') != os.environ.get('LOCUS_API_KEY'): return jsonify({'message': 'Please use a valid API Key!'}), 401
    if not request.args.get('articleId'): return jsonify({'message': 'Please specify an articleId to update!'}), 400

    article = Article.query.filter_by(articleId=request.args.get('articleId').strip()).first()
    if not article: return jsonify({'message': 'No article found with specified ID.'}), 400

    data = request.get_json()
    article.title = data['title']
    article.bodyText = data['title']
    article.datePosted = data['articleLink']
    # article.description = data['description']
    article.datePublished = datetime.datetime.now()

    db.session.commit()
    return jsonify({'message': 'Article updated successfully.'}), 200

@app.route('/admin/delete', methods=['DELETE'])
def adminDelete():
    if not request.args.get('API_KEY') or request.args.get('API_KEY') != os.environ.get('LOCUS_API_KEY'): return jsonify({'message': 'Please use a valid API Key!'}), 401
    if not request.args.get('articleId'): return jsonify({'message': 'Please specify an articleId to delete!'}), 400
