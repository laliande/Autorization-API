from flask import Flask
from apiRoutes import api

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(api, url_prefix='/api')
