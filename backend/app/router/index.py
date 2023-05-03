from flask import Blueprint, jsonify, request
from ..models import Article, User


api = Blueprint('index', __name__)

@api.route('/getArticles', methods=['GET', 'POST'])
def get_articles():
    query = request.args.get('q')
    if query:
        articles = Article().query_article(query)
    else:
        articles = Article().fetch_all()
    return {'status': 0, 'data': [article.serialize_abstract() for article in articles]}


@api.route('/getArticle', methods=['GET', 'POST'])
def get_article():
    article_id = request.json.get('articleId')
    article = Article().get_article(id=article_id)
    if article:
        return jsonify({'status': 0, 'data': article.serialize()})
    else:
        return jsonify({'status': 1, 'msg': 'Article does not exist'})

@api.route('/getSiteData', methods=['GET', 'POST'])
def get_site_data():
    return jsonify({'status': 0, 'data': {'articleCnt': Article().get_article_cnt(), 'userCnt': User().get_user_cnt()}})
