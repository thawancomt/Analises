from tinydb import Query


class users():
    def __init__(self, username: str, password: str, ip: str = None, status: bool = False):
        self.username = username
        self.password = password
        self.ip = ip
        self.status = status

    def check_user_exists(self, database, username):
        result = database.search(Query().email == username)
        print(result)
        if result:
            return True

    def create_user(self, database, username, password):

        if not self.check_user_exists(database, username):

            database.insert({'username': username,
                            'password': password})

        else:
            return redirect('login')

    def login(self):
        self.status = True

    def logout(self):
        self.status = False
