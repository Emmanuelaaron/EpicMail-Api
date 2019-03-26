from api.models.users_model import User, users
from flask import jsonify, request
import jwt
from api.validators import Validators
from api.token.jwt_token import authenticate

Validator = Validators()
auth = authenticate()
class UserController:
    def signup_user(self):
        try:
            data = request.get_json()
            email = data.get("email")
            firstname = data.get("firstname")
            lastname = data.get("lastname")
            password = data.get("password")

            user_details = [email, firstname, lastname, password]
            errors = Validator.validate(user_details, email)
            if len(errors) > 0:
                return jsonify({"errors": errors}), 400
            for user in users:
                if user["email"] == email:
                    return jsonify({"messages": "Opps!.. ..Email already exists!"}), 400
            my_account = User(email, firstname, lastname, password)
            my_account = my_account.signup()
            my_account["user_id"] = len(users) + 1
            users.append(my_account)
            return jsonify({"message": "You've sucessfully created an account"}), 201
        except Exception as e:
            e = {"Format": "Request format is invalid"}
            return jsonify(e), 400
    
    def user_signin(self):
        try:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")
            user_details = [email, password]
            for detail in user_details:
                if detail.isspace() or len(detail) == 0:
                    return jsonify({"missing": "All fields must be filled"}), 400
            if len(users) == 0:
                return jsonify({"message": "You don't have an account! please signup!"}), 200
            true_user = [user for user in users if user["email"] == email and user["password"] == password]
            if true_user:
                token = auth.encode_auth_token(email).decode("utf-8")
                return jsonify({"token": token, "message": "sucessfully logged in"}), 201
            return jsonify({"message": "Oops... Invalid login credentials"}), 400
        except Exception as e:
            e = {"Format": "Request format is invalid"}
            return jsonify(e), 400

    def get_users(self):
        return jsonify(users)