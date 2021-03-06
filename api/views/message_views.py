from flask import Blueprint, request, jsonify
from api.controllers.message_controller import message_controller
from api import app
from functools import wraps
import jwt


message_blueprint = Blueprint("messages", __name__, url_prefix="/api/v2")
message = message_controller()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({
                "status": 401,
                "error": "token missing"
            }), 401
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            user_email = data["email"]
        except:
            return jsonify({
                "message": "invalid token!"
            }), 401
        return f(user_email, *args, **kwargs)
    return decorated

@message_blueprint.route("/messages", methods=['POST'])
@token_required
def send_message(user_email):
    return message.send_email()

@message_blueprint.route("/messages")
@token_required
def get_all_received_email(user_email):
    return message.get_all_received_emails()

@message_blueprint.route("messages/<int:message_id>")
@token_required
def get_specific_message(user_email, message_id):
    return message.get_specific_email(message_id)
  
@message_blueprint.route("messages/sent")
@token_required
def get_all_sent_emails(user_email):
    return message.get_sent_emails()
  
@message_blueprint.route("/messages/<int:message_id>", methods=['DELETE'])
@token_required
def delete_email(user_email, message_id):
    return message.delete_specific_email(message_id) 

@message_blueprint.route("/groups", methods=['POST'])
@token_required
def create_group(user_email):
    return message.create_group()

@message_blueprint.route("/groups/<int:group_id>", methods=['DELETE'])
@token_required
def delete_group(user_email, group_id):
    return message.delete_specific_group(group_id)

@message_blueprint.route("/groups/<int:group_id>/users", methods=['POST'])
@token_required
def add_user_to_a_group(user_email, group_id):
    return message.add_user_to_group(group_id)

@message_blueprint.route("/groups/<int:group_id>/users/<int:user_id>", methods=["DELETE"])
@token_required
def delete_user_from_group(user_email, group_id, user_id):
    return message.delete_user_from_a_group(group_id, user_id)

@message_blueprint.route("/groups/<int:group_id>/messages", methods=["POST"])
@token_required
def send_message_to_a_group(user_email, group_id):
    return message.send_email_to_a_group(group_id)

@message_blueprint.route("/groups")
@token_required
def get_all_groups(user_email):
    return message.get_all_groups()