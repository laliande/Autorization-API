from flask import Blueprint
from flask import request
from flask import Response
from flask_bcrypt import Bcrypt, generate_password_hash
from json import dumps
from login.registration import Login
from login.response import *


api = Blueprint('api', __name__)


@api.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        login = request.form.get('login')
        hashedPassword = generate_password_hash(
            request.form.get('password')).decode('utf-8')
        user = Login(name, surname, email, login, hashedPassword)
        user.addRecordToBD()
        return Response(dumps(restonse201),  mimetype='application/json')
    return Response(dumps(restonse405),  mimetype='application/json')
