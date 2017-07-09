from flask_restful import Resource
from werkzeug.exceptions import abort
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import or_, and_
from app import db, bcrypt, jwt
from app.models import Thread, Replies, User
from app.schemas import ThreadsSchema, ThreadSchema, ReplySchema


threads_schema = ThreadsSchema(many=True)
thread_schema = ThreadSchema()
reply_schema = ReplySchema(many=True)


class UserObject:
    def __init__(self, username, id, email):
        self.username = username
        self.id = id
        self.email = email

@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'id': user['id'], 'email': user['email']}

class ThreadApi(Resource):
    """"""
    def get(self, id):
        thread = Thread.query.filter_by(id=id).first()
        if thread is None:
            abort(404)
        result = thread_schema.dump(thread)
        return jsonify(result.data)

class ThreadListApi(Resource):
    def get(self):
        threads = Thread.query.all()
        if threads is None:
            abort(404)
        result = threads_schema.dump(threads)
        return jsonify(result.data)
    @jwt_required    
    def post(self):
        currentUser = get_jwt_identity();
        requestData = request.get_json()
        thread = Thread(title=requestData['title'], body=requestData['body'], user_id=currentUser['id'])
        db.session.add(thread)
        db.session.commit()
        result = thread_schema.dump(thread)
        return jsonify(result.data)


class ReplyApi(Resource):
    """
    Every thread can have a reply
    """
    @jwt_required
    def post(self):
        currentUser = get_jwt_identity();
        requestData = request.get_json()
        reply = Replies(thread_id=requestData['thread'], body=requestData['body'], user_id=currentUser['id'])
        db.session.add(reply)
        db.session.commit()

class RegisterApi(Resource):
    def post(self):
        requestData = request.get_json()
        user = User.query.filter(or_(User.email==requestData['email'], User.username==requestData['username'])).first()
        if user is None:
            user = User(email=requestData['email'], username=requestData['username'],
                        password=bcrypt.generate_password_hash(requestData['password']))
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            regUser = UserObject(username=requestData['username'], id=user.id, email=requestData['email'])
            token = {"access_token": create_access_token(regUser.__dict__)}
            return jsonify(token)
        return jsonify({'Error':' User already exists'})

class LoginApi(Resource):
    def post(self):
        requestData = request.get_json()
        user = User.query.filter_by(email=requestData['email']).first()
        if user is None:
            return jsonify({'Error':' email or password invalid'})
        correctPassword = bcrypt.check_password_hash(user.password, requestData['password'])
        if not correctPassword:
            return jsonify({'Error':' email or password invalid'})
        regUser = UserObject(user.username, user.id, user.email)    
        token = {"access_token": create_access_token(regUser.__dict__)}
        return jsonify(token)

