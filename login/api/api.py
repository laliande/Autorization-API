from flask import Blueprint
from flask import request
from flask import Response
from json import dumps
from login.registration import Login

api = Blueprint('api', __name__)


@api.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        login = request.form.get('login')
        password = request.form.get('password')
        user = Login(name, surname, email, login, password)
        user.addRecordToBD()
        response = {'status': 201, 'response': 'Created'}
        return Response(dumps(response),  mimetype='application/json')
