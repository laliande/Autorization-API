from functools import wraps
from flask import Response, request
from json import dumps


def loginMiddleware(func):
    @wraps(func)
    def decoratorFunc(*args, **kwargs):
        token = request.authorization['token']
        if token == 'qwer':
            return func(*args, **kwargs)
        return Response(dumps({'response': 'Authorization failed'}), status=401, mimetype='application/json')
    return decoratorFunc
