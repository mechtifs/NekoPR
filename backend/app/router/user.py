from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from ..models import User, Favorite, Article
from ..utils import generate_captcha, validate_captcha

api = Blueprint('user', __name__)

@api.route('/login', methods=['POST'])
def login():
    print(request.json)
    username = request.json.get('username')
    password = request.json.get('password')
    captcha = request.json.get('captcha')
    if not username or not password or not captcha:
        return jsonify({'status': 1, 'msg': 'Missing parameters'})
    if not validate_captcha(captcha):
        return jsonify({'status': 1, 'msg': 'Wrong captcha'})
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'status': 1, 'msg': 'Username or password mismatch'})
    if user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'status': 0, 'msg': 'Successfully logged in', 'data': access_token})
    else:
        return jsonify({'status': 1, 'msg': 'Username or password mismatch'})

@api.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    captcha = request.json.get('captcha')
    if not username or not password or not captcha:
        return jsonify({'status': 1, 'msg': 'Missing parameters'})
    if not validate_captcha(captcha):
        return jsonify({'status': 1, 'msg': 'Wrong captcha'})
    if len(username) < 3 or len(username) > 20:
        return jsonify({'status': 1, 'msg': 'Username length should be between 3 and 20'})
    if len(password) < 3 or len(password) > 20:
        return jsonify({'status': 1, 'msg': 'Password length should be between 3 and 20'})
    if not username.isalnum():
        return jsonify({'status': 1, 'msg': 'Username should only contain letters and numbers'})
    user = User()
    if user.check_exist(username):
        return jsonify({'status': 1, 'msg': 'Username already exists'})
    else:
        password = user.encode_password(password)
        user = User(username=username, password=password, nickname=username)
        user.add_user()
        current_app.logger.info('User {} registered'.format(username))
        access_token = create_access_token(identity=user.id)
        return jsonify({'status': 0, 'msg': 'Successfully registered', 'data': access_token})

@api.route('/getInfo', methods=['POST'])
@jwt_required()
def get_user_info():
    print(request.headers)
    user = User().get_user(get_jwt_identity())
    return jsonify({'status': 0, 'data': user.serialize()})

@api.route('/updInfo', methods=['POST'])
@jwt_required()
def upd_user_info():
    user = User().get_user(get_jwt_identity())
    nickname = request.json.get('nickname')
    if nickname:
        user.nickname = nickname
    email = request.json.get('email')
    if email:
        user.email = email
    description = request.json.get('description')
    if description:
        user.description = description
    user.upd_user()
    return jsonify({'status': 0, 'data': user.serialize()})

@api.route('/updPwd', methods=['POST'])
@jwt_required()
def upd_user_pwd():
    user = User().get_user(get_jwt_identity())
    old_password = request.json.get('oldPassword')
    new_password = request.json.get('newPassword')
    if not old_password or not new_password:
        return jsonify({'status': 1, 'msg': 'Missing parameters'})
    if len(new_password) < 3 or len(new_password) > 20:
        return jsonify({'status': 1, 'msg': 'Password length should be between 3 and 20'})
    if user.check_password(old_password):
        user.password = user.encode_password(new_password)
        user.upd_user()
        return jsonify({'status': 0, 'msg': 'Success'})
    else:
        return jsonify({'status': 1, 'msg': 'Password error'})

@api.route('/getFavs', methods=['POST'])
@jwt_required()
def get_favs():
    user = User().get_user(get_jwt_identity())
    return jsonify({'status':0, 'data': [Article().get_article(i).serialize_abstract() for i in user.get_favs()]})

@api.route('/getFavIds', methods=['POST'])
@jwt_required()
def get_fav_ids():
    user = User().get_user(get_jwt_identity())
    return jsonify({'status': 0, 'data': user.get_favs()})

@api.route('/addFav', methods=['POST'])
@jwt_required()
def add_fav():
    article_id = request.json.get('articleId')
    user = User().get_user(get_jwt_identity())
    if Favorite().get_favorite(user_id=user.id, article_id=article_id):
        return jsonify({'status': 1, 'msg': 'Favorite exists'})
    else:
        Favorite(user_id=user.id, article_id=article_id).add_favorite()
        return jsonify({'status': 0, 'msg': 'Success'})

@api.route('/delFav', methods=['POST'])
@jwt_required()
def del_fav():
    article_id = request.json.get('articleId')
    user = User().get_user(get_jwt_identity())
    favorite = Favorite().get_favorite(user_id=user.id, article_id=article_id)
    print(user.id, article_id, favorite)
    if favorite:
        favorite.del_favorite()
        return jsonify({'status': 0, 'msg': 'Success'})
    else:
        return jsonify({'status': 1, 'msg': 'Favorite does not exist'})

@api.route('/chkFav', methods=['POST'])
@jwt_required()
def chk_fav():
    article_id = request.json.get('articleId')
    user = User().get_user(get_jwt_identity())
    if Favorite().get_favorite(user_id=user.id, article_id=article_id):
        return jsonify({'status': 0, 'data': True})
    else:
        return jsonify({'status': 0, 'data': False})

@api.route('/genCaptcha', methods=['POST'])
def gen_captcha():
    return jsonify({'status': 0, 'data': generate_captcha()})
