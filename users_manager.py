from tinydb import Query


class Users():
    from flask import redirect

    def __init__(self, email: str, password: str, username: str = None,
                 status: bool = False, admin: bool = False):
        self.username = username
        self.email = email
        self.password = password
        self.status = status
        self.admin = admin

    def check_user_exists(self, database, email):
        result = database.search(Query().email == email)

        if result:
            return True

    def create_user(self, db, username, email, password):
        if not self.check_user_exists(db, self.username):

            if self.username != '' and self.password != '' and len(self.password) > 7:
                db.insert({'username': username,
                           'email': email,
                           'password': password,
                           'admin': self.admin})

        else:
            self.login()

    def login(self):
        self.status = True

    def logout(self):
        self.status = False
