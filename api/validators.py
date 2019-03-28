from flask import request
import re

class Validators:
    def __init__(self):
        self.errors = []

    def validate_request(self):
        if not request.json:
            self.errors.append({"format": "No data inserted!"})
            return False
        return True

    def validate_email(self, email):
        email_validator = re.compile("(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)")
        if not email_validator.match(email):
            self.errors.append({"message": "Invalid email"})
    
    def validate_input_fields(self, details):
        for detail in details:
            if detail.isspace() or len(detail) == 0:
                self.errors.append({"missing": "All fields must be filled"})

    def validate(self, details, email):
        if self.validate_request():
            self.errors.clear()
            self.validate_input_fields(details)
            self.validate_email(email)
        return self.errors
