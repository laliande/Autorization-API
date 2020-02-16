from flask import Flask
from login.api.api import api

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(api, url_prefix='/api')
