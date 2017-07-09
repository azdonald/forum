from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)
marsh = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


from app.controllers import ThreadListApi, ThreadApi, RegisterApi,LoginApi, ReplyApi
api.add_resource(ThreadListApi, '/api/v1/post', endpoint='posts')
api.add_resource(RegisterApi, '/api/v1/register', endpoint='register')
api.add_resource(LoginApi, '/api/v1/login', endpoint='login')
api.add_resource(ReplyApi, '/api/v1/reply', endpoint='reply')
api.add_resource(ThreadApi, '/api/v1/post/<string:id>', endpoint='post')


