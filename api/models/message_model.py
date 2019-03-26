import datetime

messages = []      

class Message():
    
    def __init__(self, subject, message):
        self.subject = subject
        self.message = message


    def create_message(self):
        return {
            "subject": self.subject,
            "message": self.message,
            "status": "draft",
            "createdOn":  datetime.date.today()

        }

