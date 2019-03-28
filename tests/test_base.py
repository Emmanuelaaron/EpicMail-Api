import unittest
from api import app
from flask import json
from database.db import Database_connection

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        self.db = Database_connection()
        self.db.create_tables()
        self.user = {
            "email": "emmanuel@gmail.com",
            "firstname": "emmanuel",
            "lastname": "isabirye",
            "password": "12323q"
        }
        self.user2 = {
            "email": "isa@gmail.com",
            "firstname": "sonibil",
            "lastname": "kironde",
            "password": "12345"
        } 
        self.user3 = {
            "email": "isa@gmail.com",
            "firstname": "sonibil",
            "lastname": "kironde",
            "password": "12345"
        }
        self.user4 = {
            "email": "hjdgh",
            "firstname": "sonibil",
            "lastname": "kironde",
            "password": "12345"
        }
        self.user5 = {
            "email": "",
            "firstname": "emmerson",
            "lastname": "isa",
            "password": "254df"
        }
        self.user6 = {
            "email": "emma@gmail.com",
            "firstname": 0,
            "lastname": "sabuela",
            "passwor":1
        }
        self.user7 = {
            "email": "sonibil@gmail.com",
            "firstname": "sonibil",
            "lastname": "isabirye",
            'password': "uhyd7y"
        }
        self.user8 = {
            "email": "ronaldo@gmail.com",
            "firstname": "sonibil",
            "lastname": "kironde",
            "password": "12345"
        }
        self.user9 = {
            "email": "jeninah@gmail.com",
            "firstname": "sonibil",
            "lastname": "kironde",
            "password": "12345"
        }
        self.user10 = {
            "email": "rita@gmail.com",
            "firstname": "sonibil",
            "lastname": "kironde",
            "password": "12345"
        }
        self.user11 = {
            "email": "charlese@gmail.com",
            "firstname": "sonibil",
            "lastname": "kironde",
            "password": "12345"
        }
        self.user12 = {
            "email": "kirunda@gmail.com",
            "firstname": "sonibil",
            "lastname": "kironde",
            "password": "12345"
        }
        self.user13 = {
            "email": "abel@gmail.com",
            "firstname": "sonibil",
            "lastname": "kironde",
            "password": "12345"
        }

        self.message1 = {
            "subject": "people",
	        "message": "blah blah, blaha",
	        "receiver_id": 2
        }
        self.message2 = {
            "subject": "people",
	        "message": "blah blah, blaha",
	        "receiver_id": 78738783
        }
        self.user_login = {
            "email": "emmanuel@gmail.com",
            "password": "12323q"
        }
        self.message3 = {
            "subject": "  ",
	        "message": "blah blah",
	        "receiver_id": 2
        }
        self.group1 = {"group_name": "andela"}

        self.group2 = {"group_name": "andela21"}
        
        self.signup_user(self.user)
        self.token = self.login_user(self.user_login)

    def signup_user(self, user):
        signedup_user = app.test_client(self).post("/api/v2/auth/signup", 
        content_type="application/json", data=json.dumps(user))
        return signedup_user

    def login_user(self, user):
        loggedin_user = app.test_client(self).post("api/v2/auth/login",
        content_type="application/json", data=json.dumps(user))
        token = json.loads(loggedin_user.data.decode())
        return token.get("token")

    def tearDown(self):
        self.db.drop_tables()

