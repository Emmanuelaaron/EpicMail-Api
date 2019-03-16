from flask import Blueprint
from api.controllers.users_controllers import UsersController


users_blueprint = Blueprint("Users", __name__, url_prefix="/api/v1")

@users_blueprint.route('/')
def index():
    return "You're welcome to EpicMail"

@users_blueprint.route('/auth/signup', methods=["POST"])
def signup_user():
    return UsersController().signup_user()