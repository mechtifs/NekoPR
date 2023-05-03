from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, Article
from ..utils import generate_password


api = Blueprint('admin', __name__)

@api.route('/getUsers', methods=['POST'])
@jwt_required()
def get_users():
    admin_id = get_jwt_identity()
    admin = User().get_user(admin_id)
    if admin.role != 1:
        return jsonify({'status': 1, 'msg': 'Unauthorized'})
    users = User().fetch_all()
    return jsonify({'status': 0, 'data': [user.serialize() for user in users]})

@api.route('/delUser', methods=['POST'])
@jwt_required()
def del_user():
    admin_id = get_jwt_identity()
    admin = User().get_user(admin_id)
    if admin.role != 1:
        return jsonify({'status': 1, 'msg': 'Unauthorized'})
    userId = request.json.get('userId')
    user = User().get_user(userId)
    if not user:
        return jsonify({'status': 1, 'msg': 'User does not exist'})
    else:
        user.del_user()
        return jsonify({'status': 0, 'msg': 'Success'})

@api.route('/rstUserPwd', methods=['POST'])
@jwt_required()
def rst_user_pwd():
    admin_id = get_jwt_identity()
    admin = User().get_user(admin_id)
    if admin.role != 1:
        return jsonify({'status': 1, 'msg': 'Unauthorized'})
    userId = request.json.get('userId')
    user = User().get_user(userId)
    if not user:
        return jsonify({'status': 1, 'msg': 'User does not exist'})
    else:
        password = generate_password()
        user.password = user.encode_password(password)
        user.upd_user()
        return jsonify({'status': 0, 'data': password})

@api.route('/addArticle', methods=['POST'])
@jwt_required()
def add_article():
    admin_id = get_jwt_identity()
    admin = User().get_user(admin_id)
    if admin.role != 1:
        return jsonify({'status': 1, 'msg': 'Unauthorized'})
    Article(title=request.json.get('title'), content=request.json.get('content')).add_article()
    return jsonify({'status': 0, 'msg': 'Success'})

@api.route('/delArticle', methods=['POST'])
@jwt_required()
def del_article():
    admin_id = get_jwt_identity()
    admin = User().get_user(admin_id)
    if admin.role != 1:
        return jsonify({'status': 1, 'msg': 'Unauthorized'})
    article = Article().get_article(request.json.get('articleId'))
    if article:
        article.del_article()
        return jsonify({'status': 0, 'msg': 'Success'})
    else:
        return jsonify({'status': 1, 'msg': 'Article does not exist'})

@api.route('/updArticle', methods=['POST'])
@jwt_required()
def upd_article():
    admin_id = get_jwt_identity()
    admin = User().get_user(admin_id)
    if admin.role != 1:
        return jsonify({'status': 1, 'msg': 'Unauthorized'})
    article = Article().get_article(request.json.get('articleId'))
    if article:
        article.title = request.json.get('title')
        article.content = request.json.get('content')
        print(article.title, article.content)
        article.upd_article()
        return jsonify({'status': 0, 'msg': 'Success'})
    else:
        return jsonify({'status': 1, 'msg': 'Article does not exist'})
