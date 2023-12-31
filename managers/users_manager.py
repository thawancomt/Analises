from tinydb import Query, TinyDB
from datetime import datetime, date

usersdb = TinyDB('managers/databases/users.json', indent=4)


class Users():
    from flask import redirect

    def __init__(self,
                 email: str = '',
                 password: str = '',
                 username: str = '',
                 status: str = '',
                 admin: bool = False,
                 store: int = 0,
                 database: TinyDB = usersdb):

        self.username = username
        self.email = email
        self.password = password
        self.status = status
        self.admin = admin
        self.database = database
        self.last_login = date.today()
        self.store = store

        def preload_user_info_by_email():
            try:
                base = self.database.search(Query().email == self.email)[0]

                self.username = base['username']
                self.admin = base['admin']
                self.store = base['store']

                return True
            except:
                return False

        def preload_user_info_by_user():
            try:
                base = self.database.search(
                    Query().username == self.username)[0]

                self.email = base['email']
                self.admin = base['admin']
                self.store = base['store']

                return True
            except:
                return False

        if not preload_user_info_by_email():
            preload_user_info_by_user()

    def check_user_exists(self, username):
        result = self.database.search((Query().username == username))

        if result:
            return result

        else:
            return False

    def check_email_exists(self, email):
        result = self.database.search((Query().email == email))

        if result:
            return result
        else:
            return False

    def create_user(self):
        if not self.check_user_exists(self.username) or not self.check_email_exists(self.email):

            if self.username != '' and self.password != '' and len(self.password) > 7:
                self.database.insert({'username': self.username,
                                      'email': self.email,
                                      'password': self.password,
                                      'admin': self.admin,
                                      'store': self.store})
                self.status = 'User created successfully'
            else:
                self.status = 'Verify your entrys'

        else:
            if self.check_user_exists(self.username):
                self.status = 'User Already exists'
            elif self.check_email_exists(self.email):
                self.status = 'Email already exists'

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
            user_data = self.check_email_exists(self.email)[0]

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

    def edit_user_info(self, username):
        if self.check_user_exists(username):
            self.database.update({
                'username': self.username,
                'email': self.email,
                'password': self.password,
                'store': self.store
            }, Query().username == username)


t = Users(username='Thawan Henrique')


print()
