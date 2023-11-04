from tinydb import Query


class users():
    from flask import redirect

    def __init__(self, username: str, password: str, ip: str = None,
                 status: bool = False, admin: bool = False):
        self.username = username
        self.password = password
        self.ip = ip
        self.status = status
        self.admin = admin

    def check_user_exists(self, database, username):
        result = database.search(Query().email == username)

        if result:
            return True

    def create_user(self, db, username, password):
        if not self.check_user_exists(db, username):

            if self.username != '' and self.password != '' and len(self.password) > 7:
                db.insert({'email': username,
                           'password': password,
                           'admin': self.admin})

        else:
            self.login()

    def login(self):
        self.status = True

    def logout(self):
        self.status = False
