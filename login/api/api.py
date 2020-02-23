from flask import Blueprint
from flask import request
from flask import Response
from flask_bcrypt import generate_password_hash, check_password_hash
from json import dumps
from login.registration import Login, collection
from datetime import datetime, timedelta
from time import time
import jwt
from config import SECRET_KEY

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
def registration():
    try:
        if (CreateUser()):
            return Response(dumps({'response': 'sucsess create user'}), status=201,  mimetype='application/json')
        else:
            return Response(dumps({'response': 'this email or login are in BD'}), status=404, mimetype='application/json')
    except:
        return Response(dumps({'response': 'user no created. Pleace, check availability all field'}), status=400, mimetype='application/json')


@api.route('/sign-in', methods=['GET'])
def signIn():
    auth = request.authorization
    if auth:
        try:
            login = auth.username
            password = auth.password
            findUser = list(collection.find(
                {'login': login, 'password': password}))
            if len(findUser) != 0:
                token = jwt.encode(
                    {'user': login, 'exp': datetime.now() + timedelta(minutes=30)}, SECRET_KEY, algorithm='HS256').decode('utf-8')
                return Response(dumps({'response': 'TOKEN is ' + token}), status=200, mimetype='application/json')
            return Response(dumps({'response': 'No valid login or password'}), status=400, mimetype='application/json')
        except:
            return Response(dumps({'response': 'No login or password. Pleace, check availability all field'}), status=400, mimetype='application/json')
    else:
        return Response(dumps({'response': 'Please, enter authorization data'}), mimetype='application/json')
