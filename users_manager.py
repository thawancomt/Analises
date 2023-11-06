from tinydb import Query


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
                                      'admin': self.admin})

        else:
            self.login()

    def login(self):

        user_data = self.check_user_exists()[0]

        def validate_password(data, password):
            if data['password'] == password:
                return 'Success'
            else:
                return 'Invalid password'

        if user_data:
            result = validate_password(user_data, self.password)

            if result == 'Success':
                self.username = user_data['username']
                self.admin = user_data['admin']
                self.status = 'loged'

            elif result == 'Invalid password':
                self.status = result

    def logout(self):
        self.status = False
