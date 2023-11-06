from tinydb import TinyDB, Query

usersdb = TinyDB('usears.json')

table1 = usersdb.table('users')

table2 = usersdb.table('last_login')

table1.insert({'first_name': 'John', 'last_name': 'Pedro'})

table2.insert({'user': 'John'})

print(usersdb)


de
