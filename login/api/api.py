from flask import Blueprint
from flask import request
from flask import Response
from flask_bcrypt import generate_password_hash
from json import dumps
from login.registration import Login, collection


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
    if request.method == 'POST':
        try:
            if (CreateUser()):
                return Response(dumps({'response': 'sucsess create user'}), status=201,  mimetype='application/json')
            else:
                return Response(dumps({'response': 'this email or login are in BD'}), status=404, mimetype='application/json')
        except:
            return Response(dumps({'response': 'user no created. Pleace, check availability all field'}), status=400, mimetype='application/json')
