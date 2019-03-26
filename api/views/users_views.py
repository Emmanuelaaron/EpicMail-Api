from flask import Blueprint
from api.controllers.users_controllers import UserController


users_blueprint = Blueprint("Users", __name__, url_prefix="/api/v1")
User = UserController()
@users_blueprint.route('/')
def index():
    return "You're welcome to EpicMail"

@users_blueprint.route('/auth/signup', methods=["POST"])
def signup_user():
    return User.signup_user()

@users_blueprint.route('/auth/login', methods=["POST"])
def login_user():
    return User.user_signin()

@users_blueprint.route('/users')
def get_users():
    return User.get_users()