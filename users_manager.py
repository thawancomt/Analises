from tinydb import Query
from datetime import datetime, date


class Users():
    from flask import redirect

    def __init__(self, email: str,
                 password: str = None,
                 username: str = None,
                 status: bool = False,
                 admin: bool = False,
                 database: str = None):

        self.username = username
        self.email = email
        self.password = password
        self.status = status
        self.admin = admin
        self.database = database
        self.last_login = date.today()

    def check_user_exists(self):
        result = self.database.search((Query().email == self.email))

        if result:
            return result

    def create_user(self, username, email, password):
        if not self.check_user_exists(email):

            if self.username != '' and self.password != '' and len(self.password) > 7:
                self.database.insert({'username': username,
                                      'email': email,
                                      'password': password,
                                      'admin': self.admin,
                                      'last_login': self.last_login})

        else:
            self.login()

    def login(self):

        user_data = self.check_user_exists()[0]

        def validate_password(data, password):
            if data['password'] == password:
                return 'Success'
            else:
                return 'Invalid password'

        def update_last_login():

            self.database.update(
                {'last_login': self.last_login}, (Query().email == self.email))

        if user_data:
            result = validate_password(user_data, self.password)

            if result == 'Success':
                self.username = user_data['username']
                self.admin = user_data['admin']
                self.status = 'loged'
                self.last_login = str(date.today())
                update_last_login()

            elif result == 'Invalid password':
                self.status = result

    def logout(self):
        self.status = False
