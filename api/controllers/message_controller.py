from flask import request, jsonify
from api.models.message_model import Message, messages
from api.validators import Validators
from api.controllers.users_controllers import users
from api.token.jwt_token import authenticate

auth = authenticate()
validator = Validators()

class Decoder:
    @staticmethod
    def decoded_token():
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        decoded = auth.decode_auth_token(token)
        return decoded
        

class message_controller():

    def send_email(self):
        data = request.get_json()
        subject = data.get("subject")
        message = data.get("message")
        receiver_id = data.get("receiver_id")

        info = [subject, message]
        sender_email = Decoder.decoded_token()
        sender_id = [user["user_id"] for user in users if user["email"] == sender_email][0]
        if receiver_id == sender_id:
            return jsonify({
                "message": "You can't send a message to your self"
            }), 400
        for detail in info:
            if detail.isspace() or len(detail) == 0:
                return jsonify({"missing": "All fields must be filled"}), 400
        if len(users) == 0:
            return jsonify({
                "message": "Oops No one is signedup for this email"
            })
        new_user = [user for user in users if user["user_id"] == receiver_id]
        if new_user:
            my_message = Message(subject, message)
            new_message = my_message.create_message()
            new_message["message_id"] = len(messages) + 1
            new_message["receiver_id"] = receiver_id
            new_message["sender_id"] = sender_id
            messages.append(new_message)
            return jsonify({"message": "message sent"}), 201
        return jsonify({"message": "Oops... Reciever does not exist on this app"})

    def get_all_received_emails(self):
        receiver_email = Decoder.decoded_token()
        if len([user for user in users if user["email"] == receiver_email]) == 0:
            return jsonify({
                "message": "You do not have an account here! Please signup"
            })
        receiver_id = [user["user_id"] for user in users if user["email"] == receiver_email][0]
        inbox_messages = [message for message in messages if message["receiver_id"] == receiver_id]
        if not inbox_messages:
            return jsonify({
                "status": 200,
                "message": "Oops..you do not have any messages!"
            }), 200
        return jsonify({
            "status": 200,
            "data": inbox_messages
        }), 200

    def get_specific_email(self, message_id):
        user_email = Decoder.decoded_token()
        user_id = [user["user_id"] for user in users if user["email"] == user_email][0]
        messages_ = [message for message in messages if message["message_id"] == message_id]
        if not messages_:
            return jsonify({
                "status": 200,
                "message": "message does not exist"
            })
        specific_message = messages_[0]
        if specific_message["receiver_id"] == user_id or specific_message["sender_id"] == user_id:
            return jsonify({
                "status": 200,
                "data": messages_
            })
        return jsonify({
            "message": "message does not exist",
            "status": 200
        })
      
    def get_sent_emails(self):
        sender_email = Decoder.decoded_token()
        if len([user for user in users if user["email"] == sender_email]) == 0:
            return jsonify({
                "message": "You do not have an account here! Please signup"
            })
        sender_id = [user["user_id"] for user in users if user["email"] == sender_email][0]
        sent_messages = [message for message in messages if message["sender_id"] == sender_id]
        if not sent_messages:
            return jsonify({
                "status": 200,
                "message": "Oops..you do not have any messages!"
            }), 200
        return jsonify({
            "status": 200,
            "data": sent_messages
        }), 200
      
    def delete_specific_email(self, message_id):
        user_email = Decoder.decoded_token()
        user_id = [user["user_id"] for user in users if user["email"] == user_email][0]
        messages_ = [message for message in messages if message["message_id"] == message_id]
        if not messages_:
            return jsonify({
                "status": 200,
                "message": "message does not exist"
            })
        specific_message = messages_[0]
        if specific_message["receiver_id"] == user_id or specific_message["sender_id"] == user_id:
            messages.remove(specific_message)
            return jsonify({
                "status": 200,
                "message": "message sucessfully deleted!"
            })
        return jsonify({
            "message": "message does not exist",
            "status": 200
        })
