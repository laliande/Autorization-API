from flask import Blueprint
from flask import request
from flask import Response
from flask_bcrypt import Bcrypt, generate_password_hash
from json import dumps
from login.registration import Login


api = Blueprint('api', __name__)


def createUser():
    name = request.form.get('name')
    surname = request.form.get('surname')
    email = request.form.get('email')
    login = request.form.get('login')
    hashedPassword = generate_password_hash(
        request.form.get('password')).decode('utf-8')
    user = Login(name, surname, email, login, hashedPassword)
    user.addRecordToBD()


@api.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            createUser()
            return Response(dumps({'response': 'succses create user'}), status=201,  mimetype='application/json')
        except:
            return Response(dumps({'response': 'user no created. Pleace, check availability all field'}), mimetype='application/json')
