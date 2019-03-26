from tests.test_base import BaseTest
from flask import json
from api import app

class Test_messages(BaseTest):
    def test_send_email(self):
        self.signup_user(self.user7)
        resp = app.test_client(self).post("api/v1/messages",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.message1)
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(reply["message"], "message sent")

    def test_send_email_with_receiver_not_existin(self):
        resp = app.test_client(self).post("api/v1/messages",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.message2)
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(reply["message"], "Oops... Reciever does not exist on this app")

    def test_send_email_with_empty_fields(self):
        self.signup_user(self.user8)
        resp = app.test_client(self).post("api/v1/messages",
                headers={"x-access-token": self.token},
                content_type="application/json", data=json.dumps(self.message3)
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 400)
        self.assertIn("All fields must be filled", str(reply))

    def test_get_all_received_email(self):
        resp = app.test_client(self).get("api/v1/messages",
                headers={"x-access-token": self.token},
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200)
        self.assertIn("'Oops..you do not have any messages!", str(reply))
        
    def test_get_specific_email(self):
        resp = app.test_client(self).get("api/v1/messages/1455",
                headers={"x-access-token": self.token},
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200)
        self.assertIn("message does not exist", str(reply))

    def test_get_sent_emails(self):
        resp = app.test_client(self).get("api/v1/messages/sent",
                headers={"x-access-token": self.token},
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Oops..you do not have any messages!", str(reply))
          
    def test_delete_email(self):
        resp = app.test_client(self).get("api/v1/messages/1455",
                headers={"x-access-token": self.token},
            )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200)
        self.assertIn("message does not exist", str(reply))