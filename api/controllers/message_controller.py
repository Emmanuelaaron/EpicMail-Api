from flask import request, jsonify, json
from api.validators import Validators
from database.db import Database_connection
from api.token.jwt_token import authenticate
import psycopg2

auth = authenticate()
validator = Validators()
db = Database_connection()
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
        data = json.loads(request.data)
        subject = data.get("subject")
        message = data.get("message")
        receiver_email = data.get("receiver_email")

        info = [subject, message]
        sender_email = Decoder.decoded_token()
        sender_id = db.get_user_id_by_email(sender_email)
        sender_id = sender_id.get("user_id")
        if not sender_id:
            return jsonify({
                "message": "Oops.. user not registered! Please signup",
                "status": 404
            }), 404
        if not db.check_if_user_exists_by_user_email(receiver_email):
            return jsonify({
                "message": "Oops... Reciever does not exist on this app",
                "status": 404
            }), 404
        receiver_id = db.get_user_id_by_email(receiver_email)
        receiver_id = receiver_id.get("user_id")
        if receiver_email == sender_email:
            return jsonify({
                "message": "You can't send a message to your self",
                "status": 400
            }), 400
        for detail in info:
            if detail.isspace() or len(detail) == 0:
                return jsonify({"missing": "All fields must be filled"}), 400
        
        print (sender_id)
        message = db.create_message(subject, message, receiver_id, sender_id, receiver_email, sender_email)
        return jsonify({
            "message": "message sent",
            "data": message,
            "status": 201
        }), 201

    def get_all_received_emails(self):
        receiver_email = Decoder.decoded_token()
        receiver_id = db.get_user_id_by_email(receiver_email)
        if not receiver_id:
            return jsonify({
                "message": "You do not have an account here! Please signup",
                "status": 404
            })
        receiver_id = receiver_id.get("user_id")
        inbox_messages = db.get_all_received_messages_using_receiver_id(receiver_id)
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
        user_id = db.get_user_id_by_email(user_email)
        messages_ = db.get_message_by_specific_message_id(message_id)
        if not messages_:
            return jsonify({
                "status": 404,
                "message": "message does not exist"
            }), 404
        user_id = user_id.get("user_id")
        if messages_["receiver_id"] == user_id or messages_["sender_id"] == user_id:
            return jsonify({
                "status": 200,
                "data": messages_
            }), 200
        return jsonify({
            "message": "message does not exist",
            "status": 404
        })
      
    def get_sent_emails(self):
        sender_email = Decoder.decoded_token()
        sender_id = db.get_user_id_by_email(sender_email)
        if not sender_id:
            return jsonify({
                "message": "You do not have an account here! Please signup",
                "status": 404
            }), 404
        sender_id = sender_id.get("user_id")
        sent_messages = db.get_all_sent_messages_using_sender_id(sender_id)
        if not sent_messages:
            return jsonify({
                "status": 404,
                "message": "Oops..you do not have any messages!"
            }), 404
        return jsonify({
            "status": 200,
            "data": sent_messages
        }), 200
      
    def delete_specific_email(self, message_id):
        user_email = Decoder.decoded_token()
        user_id = db.get_user_id_by_email(user_email)
        messages_ = db.get_message_by_specific_message_id(message_id)
        if not messages_:
            return jsonify({
                "status": 404,
                "message": "message does not exist"
            }), 404
        user_id = user_id.get("user_id")
        if messages_["receiver_id"] == user_id or messages_["sender_id"] == user_id:
            db.delete_specific_message(message_id)
            return jsonify({
               "message": "message sucessfully deleted"
            })
        return jsonify({
            "message": "message does not exist",
            "status": 404
        }), 404

    def create_group(self):
        try:
            user_email = Decoder.decoded_token()
            user_id = db.get_user_id_by_email(user_email)
            user_id = user_id.get("user_id")
            data = json.loads(request.data)
            group_name = data.get("group_name")
            group_in = db.check_for_a_group_whether_exists(group_name)
            print (group_in)
            if not group_in:
                db.create_group(group_name, user_id)
                db.add_user_to_a_group(user_email, group_name)
                return jsonify({
                    "message": "sucessfully created a group",
                }), 201
            if group_in[0].get("group_name") == group_name:
                return jsonify({
                    "message": "Group already exists! Please choose another name"
                })
        except Exception as e:
            return jsonify({
                "message": "No group name inserted!"
            }), 400
        

    def delete_specific_group(self, group_id):
        user_email = Decoder.decoded_token()
        user_id = db.get_user_id_by_email(user_email)
        user_id = user_id.get("user_id")
        group_name = db.get_group_name_by_group_id(group_id)
        if not group_name:
            return jsonify({
                "message": "Oops .. group does not exist!",
                "status": 404
            })
        group_name = group_name.get("group_name")
        if not db.match_user_id_and_group_id_in_groups(group_id, user_id):
            return jsonify({
                "message": "group_id does not exist",
                "status": 404
            }), 404
        db.delete_specific_group(group_id)
        db.delete_table(group_name)
        return jsonify({
            "message": "Sucessfully deleted the group!",
            "status": 200
        }), 200
    
    def add_user_to_group(self, group_id):
        user_email = Decoder.decoded_token()
        user_id = db.get_user_id_by_email(user_email)
        user_id = user_id.get("user_id")
        data = request.get_json()
        email = data.get("email")
        if not db.check_if_user_exists_by_user_email(email):
            return jsonify({
                "message": "that user is not signed up on this app!",
                "status": 404
            }), 404
        group_name = db.get_group_name_by_group_id(group_id)
        if not group_name:
            return jsonify({
                "message": "Oops .. group does not exist!",
                "status": 404
            }), 404
        createdby = db.get_user_id_from_groups_by_group_id(group_id)
        createdby = createdby.get("createdby")
        if user_id != createdby:
            return jsonify({
                "message": "Oops... you can only add users to groups created by you.",
                "status": 400
            }), 400
        group_name = group_name.get("group_name")
        if db.check_if_user_exists_in_a_group(email, group_name):
            return jsonify({
                "message": "User already added to the group!",
                "status": 200
            }), 200
        db.add_user_to_a_group(email, group_name)
        return jsonify({
            "message": email +" sucessfully added to " + group_name
        }), 201
    
    def get_all_groups(self):
        user_email = Decoder.decoded_token()
        my_groups = db.get_all_groups()
        groups = []
        real_groups = []
        for item in my_groups:
            groups.append(item.get("group_name"))
        for group in groups:
            mine_groups = db.get_groups_for_user(user_email, group)
            if mine_groups:
                real_groups.append(mine_groups)
        if len(real_groups) == 0:
            return jsonify({
                "message": "Oops .. You're not in any group!"
            })
        return jsonify({
            "message": real_groups
        })

    def delete_user_from_a_group(self, group_id, user_id):
        user_email = Decoder.decoded_token()
        log_id = db.get_user_id_by_email(user_email)
        log_id = log_id.get("user_id")
        print (log_id)
        group_name = db.get_group_name_by_group_id(group_id)
        if not group_name:
            return jsonify({
                "message": "Oops .. group does not exist!",
                "status": 404
            }), 404
        users_id = db.get_user_id_if_user_exists_by_user_id(user_id)
        if not users_id:
            return jsonify({
                "message": "Oops .. User doesn't exist",
                "status": 404
            }), 404
        createdby = db.get_user_id_from_groups_by_group_id(group_id)
        createdby = createdby.get("createdby")
        if log_id != createdby:
            return jsonify({
                "message": "Oops... you can only delete users from groups created by you.",
                "status": 400
            })
        users_id = users_id.get("user_id")
        email = db.get_email_by_user_id(users_id)
        email = email.get("email")
        group_name = group_name.get("group_name")
        if not db.check_if_user_exists_in_a_group(email, group_name):
            return jsonify({
                "message": "users does not exist!"
            })
        db.delete_user_from_a_group(email, group_name)
        return jsonify({
            "message": "Sucessfully deleted {} from {}".format(email, group_name)
        })

    def send_email_to_a_group(self, group_id):
        user_email = Decoder.decoded_token()
        user_id = db.get_user_id_by_email(user_email)
        user_id = user_id.get("user_id")
        print (user_id)
        group_name = db.get_group_name_by_group_id(group_id)
        createdby = db.get_user_id_from_groups_by_group_id(group_id)
        if not group_name:
            return jsonify({
                "message": "Oops .. group does not exist!",
                "status": 404
            }), 404
        group_name = group_name.get("group_name")
        createdby = createdby.get("createdby")
        print(createdby)
        user = db.check_if_user_exists_in_a_group(user_email, group_name)
        if not user or user_id != createdby:
            return jsonify({
                "message": "You can only send a message to a group you are part of!",
                "status": 404
            }), 404
        data = request.get_json()
        subject = data.get("subject")
        message = data.get("message")
        if not request.json:
            return jsonify({
                "message": "No data inserted!",
                "status": 400
            }), 400
        message = db.send_message_to_a_group(group_name, subject, message, user_id)
        return jsonify({
            "message": "sucessfully sent the message to " + group_name,
            "data": message,
            "status": 201
        }), 201

            