session = {
    'username': '',
    'loged': False,
}

print(session)

session.update({
    'username': 'tt',
    'loged': True,
})


print(session)
