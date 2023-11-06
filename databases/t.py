from tinydb import TinyDB, Query

usersdb = TinyDB('databases/users.json', indent=4)

result = usersdb.search((Query().email == 'thawancomt@gmail.com'))


usersdb.update({'last_login': 2}, Query().email == 'thawancomt@gmail.com')
