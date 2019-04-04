import psycopg2
import psycopg2.extras  
import os
from pprint import pprint

class Database_connection:

    def __init__(self):
        try:
            self.database_url = os.getenv("DATABASE_URL")
            self.connect = psycopg2.connect(self.database_url)
            self.connect.autocommit = True
            self.cursor = self.connect.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)
            pprint("database running")
        except Exception as e:
            print(e)
            pprint("failed to connect")
        self.create_tables()

    def create_tables(self):

        users_table = "CREATE TABLE IF NOT EXISTS users(user_id SERIAL PRIMARY KEY, email VARCHAR(50) UNIQUE, \
                        firstname VARCHAR(50), lastname VARCHAR(50), password VARCHAR(50));"

        message_table = "CREATE TABLE IF NOT EXISTS messages(message_id SERIAL PRIMARY KEY, \
                        createdOn TIMESTAMP DEFAULT NOW(), subject TEXT NOT NULL, message TEXT NOT NULL, \
                            receiver_id INTEGER REFERENCES users, sender_id INTEGER REFERENCES users,\
                                 receiver_email VARCHAR(50), sender_email VARCHAR(50));"
        
        groups_table = "CREATE TABLE IF NOT EXISTS groups(group_id SERIAL PRIMARY KEY, \
                        group_name VARCHAR(50), createdby INTEGER REFERENCES users);"

        groups_messages_table = "CREATE TABLE IF NOT EXISTS group_messages(message_id SERIAL PRIMARY KEY, \
                                group_name VARCHAR(50), subject TEXT NOT NULL, message TEXT NOT NULL, \
                                createdby INTEGER REFERENCES users, createdon TIMESTAMP DEFAULT NOW());"
        self.cursor.execute(users_table)
        self.cursor.execute(message_table)
        self.cursor.execute(groups_table)
        self.cursor.execute(groups_messages_table)

    def signup(self, email, firstname, lastname, password):
        user = "INSERT INTO users(email, firstname, lastname, password) \
                VALUES('{}', '{}', '{}', '{}') returning user_id, firstname \
                    lastname, email;".format(email, firstname, lastname, password)
        self.cursor.execute(user)
        return self.cursor.fetchone()
    
    def check_user_login(self, email, password):
        query = "SELECT * FROM users WHERE email = '{}' AND password = '{}';".format(email, password)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False

    def get_user_id_by_email(self, email):
        query = "SELECT user_id FROM users WHERE email = '{}';".format(email)
        self.cursor.execute(query)
        user_id = self.cursor.fetchone()
        return user_id if True else False
    
    def create_message(self, subject, message, receiver_id, sender_id, receiver_email, sender_email):
        message = "INSERT INTO messages(subject, message, receiver_id, sender_id, receiver_email, sender_email)\
                    VALUES('{}', '{}', '{}', '{}', '{}', '{}')returning message_id, subject,\
                    message, receiver_id, sender_id, sender_email,\
                    receiver_email;".format(subject, message, receiver_id, sender_id, receiver_email, sender_email)
        self.cursor.execute(message)
        return self.cursor.fetchone()
    
    def check_if_user_exists_by_user_id(self, user_d):
        query = "SELECT * FROM users WHERE user_id = {};".format(user_d)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result if True else False

    def check_if_user_exists_by_user_email(self, user_email):
        query = "SELECT * FROM users WHERE email = '{}';".format(user_email)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result if True else False

    def get_all_received_messages_using_receiver_id(self, receiver_id):
        query = "SELECT * FROM messages WHERE receiver_id = '{}';".format(receiver_id)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result if True else False
    
    def get_all_sent_messages_using_sender_id(self, sender_id):
        query = "SELECT * FROM messages WHERE sender_id = '{}';".format(sender_id)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result if True else False
    
    def get_message_by_specific_message_id(self, message_id):
        query = "SELECT * FROM messages WHERE message_id = {};".format(message_id)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result if True else False

    def delete_specific_message(self, message_id):
        query = "DELETE FROM messages WHERE message_id = {};".format(message_id)
        self.cursor.execute(query)
        
    def drop_tables(self):
        query = "DROP TABLE IF EXISTS {0} CASCADE"
        tables = ["users", "messages", "groups", "andela", "andela21", "peoplepower", "group_messages"]
        for table in tables:
            self.cursor.execute(query.format(table))

    def create_group(self, group_name, user_id):
        query = "CREATE TABLE {}(group_id SERIAL PRIMARY KEY, \
                members VARCHAR(50), isadmin BOOLEAN);".format(group_name)
        query2 = "INSERT INTO groups(group_name, createdby)\
                  VALUES('{}', {});".format(group_name, user_id)
        self.cursor.execute(query)
        self.cursor.execute(query2)

    def check_if_table_exists(self, table_name):
        query = "SELECT to_regclass('{}');".format(table_name)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return False if result else True
    
    def match_user_id_and_group_id_in_groups(self, group_id, user_id):
        query = "SELECT * FROM groups WHERE group_id = {} \
                AND createdby = {};".format(group_id, user_id)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result 

    def delete_specific_group(self, group_id):
        query = "DELETE FROM groups WHERE group_id = {};".format(group_id)
        self.cursor.execute(query)
    
    def delete_table(self, table_name):
        query = "DROP TABLE {};".format(table_name)
        self.cursor.execute(query)

    def get_group_name_by_group_id(self, group_id):
        query = "SELECT group_name FROM groups WHERE group_id = '{}';".format(group_id)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result if True else False
    
    def add_user_to_a_group(self, user, groupname):
        isadmin = False
        query = "INSERT INTO {}(members, isadmin)VALUES ('{}', '{}');".format(groupname, user, isadmin)
        self.cursor.execute(query)
    
    def check_if_user_exists_in_a_group(self, user_email, group_name):
        query = "SELECT * FROM {} WHERE members = '{}';".format(group_name, user_email)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return True if result else False

    def get_user_id_from_groups_by_group_id(self, group_id):
        query = "SELECT createdby FROM groups WHERE group_id = {};".format(group_id)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result if True else False

    def get_user_id_if_user_exists_by_user_id(self, user_d):
        query = "SELECT user_id FROM users WHERE user_id = {};".format(user_d)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result if True else False

    def get_email_by_user_id(self, user_id):
        query = "SELECT email FROM users WHERE user_id = '{}';".format(user_id)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result if True else False

    def delete_user_from_a_group(self, member, group_name):
        query = "DELETE FROM {} WHERE members = '{}';".format(group_name, member)
        self.cursor.execute(query)

    def send_message_to_a_group(self, group_name, subject, message, createdby):
        message = "INSERT INTO group_messages(group_name, subject, message, createdby)\
                VALUES('{}', '{}', '{}', {}) returning message_id, group_name, subject, message,\
                    createdby, createdon;".format(group_name, subject, message, createdby)
        self.cursor.execute(message)
        return self.cursor.fetchone()

    def check_if_email_exists(self, email):
        query = "SELECT * FROM users WHERE email = '{}';".format(email)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result if True else False

    def get_all_groups(self):
        query = "SELECT group_name FROM groups"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result if True else False

    def get_groups_for_user(self, email, group_name):
        query = "SELECT * FROM {} WHERE members = '{}';".format(group_name, email)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return group_name if result else False

    def check_if_group_exists(self,group_name):
        query = "SELECT * FROM {};".format(group_name)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result if True else False

    def check_for_a_group_whether_exists(self, group_name):
        query = "SELECT group_name FROM groups WHERE group_name = '{}';".format(group_name)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result if True else False





if __name__ == "__main__":
    db = Database_connection()