from functools import wraps
from flask import Response, request
from json import dumps
import jwt
from config import SECRET_KEY


def loginMiddleware(func):
    @wraps(func)
    def decoratorFunc(*args, **kwargs):
        try:
            token = request.headers['Authorization'][7:]
            try:
                jwt.decode(token, SECRET_KEY)
            except:
                return Response(dumps({'response': 'The token is not valid'}), status=403, mimetype='application/json')
            return func(*args, **kwargs)
        except:
            return Response(dumps({'response': 'The token is not difined'}), status=401,  mimetype='application/json')
    return decoratorFunc
