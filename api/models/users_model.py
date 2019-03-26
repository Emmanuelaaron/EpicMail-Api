users = []

class User:
    def __init__(self, email, firstname, lastname, password):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password

    def signup(self):
        return {"email": self.email, "firstname": self.firstname, 
            "lastname": self.lastname, "password": self.password}