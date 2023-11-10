class Session():
    connected_users = {}

    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.username = None
        self.admin = False
        self.loged = False

    def create_session(self):
        self.connected_users[self.ip_address] = {'username': self.username,
                                                 'admin': self.admin,
                                                 'loged': self.loged}

    def get_session(self):
        if self.ip_address in self.connected_users:
            return self.connected_users[self.ip_address]['username']
        else:
            return None

    def logoff(self):
        self.admin = False
        self.loged = False
        self.username = None

        self.connected_users[self.ip_address] = {'username': self.username,
                                                 'admin': self.admin,
                                                 'loged': self.loged}


if __name__ == '__main__':
    teste = Session(12)
    teste.username = 'teste'
    teste.create_session()

    print(Session(12).get_session())
