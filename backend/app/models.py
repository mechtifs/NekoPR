from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from hashlib import sha1
from .db import db


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    password = Column(String(80))
    nickname = Column(String(80))
    email = Column(String(80))
    description = Column(String(200))
    role = Column(Integer)
    favorites = relationship('Favorite', backref='user', lazy='dynamic')
    salt = '$y2tUI&GsCdey46o'

    def encode_password(self, password):
        return sha1((password+self.salt).encode('utf-8')).hexdigest()

    def check_password(self, password):
        return self.password == self.encode_password(password)

    def check_exist(self, username):
        return User.query.filter_by(username=username).first()

    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def del_user(self):
        db.session.delete(self)
        db.session.commit()

    def upd_user(self):
        db.session.commit()

    def get_user(self, id):
        return User.query.filter_by(id=id).first()

    def fetch_all(self):
        return User.query.all()

    def get_favs(self):
        return [favorite.article_id for favorite in self.favorites]

    def get_user_cnt(self):
        return User.query.count()

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'email': self.email,
            'description': self.description,
            'role': self.role
        }

class Article(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(80))
    content = Column(String(10000))
    image = Column(String(200))

    def add_article(self):
        db.session.add(self)
        db.session.commit()

    def del_article(self):
        db.session.delete(self)
        db.session.commit()

    def upd_article(self):
        db.session.commit()

    def get_article(self, id):
        return Article.query.filter_by(id=id).first()

    def query_article(self, query):
        return Article.query.filter(Article.title.like('%'+query+'%')).all()

    def fetch_all(self):
        return Article.query.all()

    def get_article_cnt(self):
        return Article.query.count()

    def serialize_abstract(self):
        return {
            'id': self.id,
            'title': self.title,
            'abstract': ' '.join(self.content[:100].split()[:-1])+'...',
            'image': self.image
        }

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'image': self.image
        }

class Favorite(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    article_id = Column(Integer, ForeignKey('article.id'))

    def add_favorite(self):
        db.session.add(self)
        db.session.commit()

    def del_favorite(self):
        db.session.delete(self)
        db.session.commit()

    def upd_favorite(self):
        db.session.commit()

    def get_favorite(self, user_id, article_id):
        return Favorite.query.filter_by(user_id=user_id, article_id=article_id).first()

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'article_id': self.article_id
        }