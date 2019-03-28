from tests.test_base import BaseTest
from flask import json
from api import app

class Test_messages(BaseTest):
    def test_send_email(self):
        self.signup_user(self.user7)
        resp = app.test_client(self).post("api/v2/messages",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.message1)
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(reply["message"], "message sent")

    def test_send_email_with_receiver_not_existin(self):
        resp = app.test_client(self).post("api/v2/messages",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.message2)
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(reply["message"], "Oops... Reciever does not exist on this app")

    def test_send_email_with_empty_fields(self):
        self.signup_user(self.user8)
        resp = app.test_client(self).post("api/v2/messages",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.message3)
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 400)
        self.assertIn("All fields must be filled", str(reply))

    def test_get_all_received_email(self):
        resp = app.test_client(self).get("api/v2/messages",
                headers={"x-access-token": self.token},
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200)
        self.assertIn("'Oops..you do not have any messages!", str(reply))
        
    def test_get_specific_email(self):
        resp = app.test_client(self).get("api/v2/messages/1455",
                headers={"x-access-token": self.token},
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 404)
        self.assertIn("message does not exist", str(reply))

    def test_get_sent_emails(self):
        resp = app.test_client(self).get("api/v2/messages/sent",
                headers={"x-access-token": self.token},
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 404)
        self.assertIn("Oops..you do not have any messages!", str(reply))
          
    def test_delete_email(self):
        resp = app.test_client(self).get("api/v2/messages/1455",
                headers={"x-access-token": self.token},
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 404)
        self.assertIn("message does not exist", str(reply))

    def test_create_group(self):
        resp = app.test_client(self).post("api/v2/groups",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.group1)
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(reply["message"], "sucessfully created a group")

    def test_create_group_with_invalid_input(self):
        resp = app.test_client(self).post("api/v2/groups",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps({"gr": 87677, "ui": "67"})
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(reply["message"], "Oops.. .Invalid input!")
    
    def test_create_group_with_identical_name(self):
        app.test_client(self).post("api/v2/groups",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.group1)
            )
        resp = app.test_client(self).post("api/v2/groups",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.group1)
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(reply["message"], "Group already exists! consider another name")



    def test_create_group_with_no_name_inserted(self):
        resp = app.test_client(self).post("api/v2/groups",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps({"group_name": "  "})
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(reply["message"], "No group name inserted!")

    def test_delete_group(self):
        app.test_client(self).post("api/v2/groups",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.group1)
            )
        resp = app.test_client(self).delete("api/v2/groups/1",
                headers={"x-access-token": self.token}
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(reply["message"], "Sucessfully deleted the group!")

    def test_delete_group_when_group_does_not_exist(self):
        app.test_client(self).post("api/v2/groups",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.group1)
            )
        resp = app.test_client(self).delete("api/v2/groups/156",
                headers={"x-access-token": self.token}
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(reply["message"], "Oops .. group does not exist!")

    def test_add_user_to_a_group(self):
        app.test_client(self).post("api/v2/groups",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.group1)
            )
        self.signup_user(self.user10)
        resp = app.test_client(self).post("api/v2/groups/1/users",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps({
                    "email": "rita@gmail.com"
                })
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(reply["message"], "rita@gmail.com sucessfully added to andela")

    def test_add_user_to_a_group_when_group_not_existing(self):
        app.test_client(self).post("api/v2/groups",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.group1)
            )
        self.signup_user(self.user10)
        resp = app.test_client(self).post("api/v2/groups/134/users",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps({
                    "email": "rita@gmail.com"
                })
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(reply["message"], "Oops .. group does not exist!")

    def test_add_user_to_a_group_with_non_existing_user(self):
        app.test_client(self).post("api/v2/groups",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.group1)
            )
        self.signup_user(self.user10)
        resp = app.test_client(self).post("api/v2/groups/1/users",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps({
                    "email": "ritajhjh@gmail.com"
                })
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(reply["message"], "that user is not signed up on this app!")

    def test_add_user_second_time_to_a_group_with_non_existing_user(self):
        app.test_client(self).post("api/v2/groups",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.group1)
            )
        self.signup_user(self.user10)
        app.test_client(self).post("api/v2/groups/1/users",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps({
                    "email": "rita@gmail.com"
                })
            )
        resp = app.test_client(self).post("api/v2/groups/1/users",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps({
                    "email": "rita@gmail.com"
                })
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(reply["message"], "User already added to the group!")

    def test_delete_user_from_a_group(self):
        app.test_client(self).post("api/v2/groups",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.group1)
            )
        self.signup_user(self.user11)
        app.test_client(self).post("api/v2/groups/1/users",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps({
                    "email": "charlese@gmail.com"
                })
            )
        resp = app.test_client(self).delete("api/v2/groups/1/users/2",
                headers={"x-access-token": self.token},
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(reply["message"], "Sucessfully deleted charlese@gmail.com from andela")

    def test_delete_user_from_a_group_when_group_not_existing(self):
        self.signup_user(self.user12)
        resp = app.test_client(self).delete("api/v2/groups/168/users/2",
                headers={"x-access-token": self.token},
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(reply["message"], "Oops .. group does not exist!")

    def test_delete_user_from_a_group_not_existing_user(self):
        app.test_client(self).post("api/v2/groups",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.group1)
            )
        resp = app.test_client(self).delete("api/v2/groups/1/users/277",
                headers={"x-access-token": self.token},
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(reply["message"], "Oops .. User doesn't exist")

    def test_delete_user_from_a_group_by_unauthorised_personel(self):
        app.test_client(self).post("api/v2/groups",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.group1)
            )
        self.signup_user(self.user11)
        self.signup_user(self.user13)
        app.test_client(self).post("api/v2/groups/1/users",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps({
                    "email": "charlese@gmail.com"
                })
            )
        token = self.login_user({"email": "abel@gmail.com"})
        resp = app.test_client(self).delete("api/v2/groups/1/users/2",
                headers={"x-access-token": token},
            )
        self.assertEqual(resp.status_code, 401)




