from tests.test_base import BaseTest
from flask import json
from api import app

class Test_users(BaseTest):
    def test_signup_user(self):
        resp = self.signup_user(self.user2)
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 201)
        self.assertIn("You've sucessfully created an account", str(reply))
    
    def test_signup_user_with_existing_email(self):
        self.signup_user(self.user9)
        resp = self.signup_user(self.user9)
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Email already exists! Choose another", str(reply))

    def test_signup_user_with_invalid_email(self):
        resp = self.signup_user(self.user4)
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Invalid email", str(reply))

    def test_signup_user_with_no_data_inserted(self):
        self.user = {}
        resp = self.signup_user(self.user)
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 400)
        self.assertIn("No data inserted!", str(reply))
        
    def test_signup_user_with_missing_info(self):
        resp = self.signup_user(self.user5)
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 400)
        self.assertIn("All fields must be filled", str(reply))

    def test_signup_user_with_invalid_format(self):
        resp = self.signup_user(self.user6)
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(reply["Format"], "Request format is invalid")

    def test_signin_user(self):
        resp = self.signup_user(self.user7)
        resp = app.test_client(self).post("/api/v1/auth/login",
                content_type="application/json", data=json.dumps({
                    "email": "sonibil@gmail.com",
                    "password": "uhyd7y"
                })
        )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(reply["message"], "sucessfully logged in")

    def test_signin_user_with_wrong_login_credentials(self):
        resp = self.signup_user(self.user)
        resp = app.test_client(self).post("api/v1/auth/login",
                content_type="application/json", data=json.dumps({
                    "email": "sonibil@gmail.com",
                    "password": "123423"
                }))
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(reply["message"], "Oops... Invalid login credentials")

    def test_signin_user_with_an_empty_field(self):
        resp = app.test_client(self).post("api/v1/auth/login",
                content_type="application/json", data=json.dumps({
                    "email": "",
                    "password": "5245"
                })
                )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(reply["missing"], "All fields must be filled")

    def test_signin_user_with_invalid_format(self):
        resp = app.test_client(self).post("api/v1/auth/login",
                content_type="application/json", data=json.dumps({
                    "email": "tyty",
                    "tydg": "5245",
                    "tyst": "iye"
                })
                )
        reply = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Request format is invalid", str(reply))


        