from tinydb import Query, TinyDB
from datetime import datetime, date

usersdb = TinyDB('databases/users.json', indent=4)


class Users():
    from flask import redirect

    def __init__(self,
                 email: str,
                 password: str = '',
                 username: str = '',
                 status: str = '',
                 admin: bool = False,
                 database: TinyDB = usersdb):

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

    def create_user(self):
        if not self.check_user_exists():

            if self.username != '' and self.password != '' and len(self.password) > 7:
                self.database.insert({'username': self.username,
                                      'email': self.email,
                                      'password': self.password,
                                      'admin': self.admin})
                self.status = 'User created successfully'
            else:
                self.status = 'Verify your entrys'

        else:
            self.status = 'User Already exist'

    def login(self):

        def validate_password(data, password):
            if data['password'] == password:
                return 'Success'
            else:
                return 'Invalid password'

        def update_last_login():

            self.database.update(
                {'last_login': self.last_login}, (Query().email == self.email))

        try:
            user_data = self.check_user_exists()[0]

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

        except:
            self.status = 'User not found'

    def logout(self):
        self.status = False
