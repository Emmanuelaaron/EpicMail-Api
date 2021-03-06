from database.db import Database_connection
from flask import jsonify, request, json
import jwt
from api.validators import Validators
from api.token.jwt_token import authenticate
import psycopg2

db = Database_connection()
Validator = Validators()
auth = authenticate()
class UserController:
    def signup_user(self):
        try:
            data = json.loads(request.data)
            email = data.get("email")
            firstname = data.get("firstname")
            lastname = data.get("lastname")
            password = data.get("password")

            user_details = [email, firstname, lastname, password]
            errors = Validator.validate(user_details, email)
            if len(errors) > 0:
                return jsonify({"errors": errors}), 400
            if db.check_if_email_exists(email):
                return jsonify ({
                    "status": 400,
                    "message": "Email already exists! Choose another"
                }), 400
            token = auth.encode_auth_token(email).decode("utf-8")
            user = db.signup(email, firstname, lastname, password)
            return jsonify({
                "message":  "congrats "+ firstname + "!" + " you've sucessfully signed up!",
                "status": 201,
                "data": user,
                "token": token

            }), 201
        except Exception as e:
            e = {"Format": "Request format is invalid"}
            return jsonify(e), 400
    
    def user_signin(self):
        # # try:
            data = json.loads(request.data)
            email = data.get("email")
            password = data.get("password")
            user_details = [email, password]
            for detail in user_details:
                if detail.isspace() or len(detail) == 0:
                    return jsonify({"missing": "All fields must be filled"}), 400

            if db.check_user_login(email, password):
                token = auth.encode_auth_token(email).decode("utf-8")
                return jsonify({
                    "token": token, 
                    "message": "sucessfully logged in",
                    "status": 200
                }), 200
            return jsonify({"message": "Oops... Invalid login credentials"}), 400
        # except Exception as e:
        #     e = {"Format": "Request format is invalid"}
        #     return jsonify(e), 400

