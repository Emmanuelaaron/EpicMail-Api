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
        self.assertEqual(resp.status_code, 200)
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
        self.assertEqual(resp.status_code, 200)
        self.assertIn("message does not exist", str(reply))

    def test_get_sent_emails(self):
        resp = app.test_client(self).get("api/v2/messages/sent",
                headers={"x-access-token": self.token},
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Oops..you do not have any messages!", str(reply))
          
    def test_delete_email(self):
        resp = app.test_client(self).get("api/v2/messages/1455",
                headers={"x-access-token": self.token},
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200)
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


