from flask import Flask, Blueprint
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = "I Love what I am seeing"

from api.views.users_views import users_blueprint
app.register_blueprint(users_blueprint)

from api.views.message_views import message_blueprint
app.register_blueprint(message_blueprint)
