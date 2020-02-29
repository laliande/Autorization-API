from flask import Blueprint
from flask import request
from flask import Response
from flask_bcrypt import generate_password_hash, check_password_hash
from json import dumps
from registration import Login, collection
from datetime import datetime, timedelta
import jwt
from config import SECRET_KEY
from middlewares import loginMiddleware

api = Blueprint('api', __name__)


def CreateUser():
    email = request.form.get('email')
    login = request.form.get('login')
    name = request.form.get('name')
    surname = request.form.get('surname')
    hashedPassword = generate_password_hash(
        request.form.get('password')).decode('utf-8')
    user = Login(name, surname, email, login, hashedPassword)
    try:
        user.addRecordToBD()
        return True
    except:
        return False


@api.route('/sign-up', methods=['POST'])
def signUp():
    try:
        if (CreateUser()):
            return Response(dumps({'response': 'sucsess create user'}), status=201,  mimetype='application/json')
        else:
            return Response(dumps({'response': 'this email or login are in BD'}), status=404, mimetype='application/json')
    except:
        return Response(dumps({'response': 'user no created. Pleace, check availability all field'}), status=400, mimetype='application/json')


@api.route('/sign-in', methods=['POST'])
def signIn():
    login = request.form.get('login')
    password = request.form.get('password')
    users = list(collection.find({'login': login}))
    if len(users) != 0:
        for IUser in range(len(users)):
            if users[IUser].get('login') == login:
                hashedPassword = users[IUser].get('password')
                break
        if check_password_hash(hashedPassword, password):
            token = jwt.encode(
                {'user': login, 'exp': datetime.now() + timedelta(minutes=30)}, SECRET_KEY, algorithm='HS256').decode('utf-8')
            return Response(dumps({'response': 'Your token: ' + token}), status=200, mimetype='application/json')
        else:
            return Response(dumps({'response': 'No invalid this password'}), status=404, mimetype='application/json')
    else:
        return Response(dumps({'response': 'No this login in BD'}), status=400, mimetype='application/json')


@api.route('/protected', methods=['GET'])
@loginMiddleware
def protected():
    return Response(dumps({'response': 'Authentication is successful'},), status=200, mimetype='application/json')
