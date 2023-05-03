from flask import Flask
import logging
from logging import FileHandler
from .db import init_db
from .jwt import init_jwt
from .router import index_api, user_api, admin_api


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Kn@y^CKf5Vu4D#pe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@mysql/test'
app.config['JWT_SECRET_KEY'] = '9fm#Q*rn9Y1ue1L%'

init_db(app)
init_jwt(app)

file_handler = FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

app.logger.addHandler(file_handler)

app.register_blueprint(index_api)
app.register_blueprint(user_api, url_prefix='/user')
app.register_blueprint(admin_api, url_prefix='/admin')
