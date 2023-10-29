"""Some methods needs conection with the modules imported from main"""
from tinydb import Query, TinyDB

db = TinyDB('databases/dados.json')
store_list = {3: 'Colombo',
              5: 'Odivelas',
              11: 'Campo de Ourique',
              13: 'Coina',
              25: 'Baixa Chiado'}


def get_billing(store, date):
    billing = db.search((Query().store == store) &
                        (Query().date == date))
    return billing[0]['billing']


def get_production(store, date):
    production = db.search((Query().store == store) &
                           (Query().date == date))
    return production[0]['production']


def get_usage(store, date):
    usage = db.search((Query().store == store) &
                      (Query().date == date))
    return usage


def define_store(store):
    stores = {5: 'Odivelas',
              3: 'Colombo',
              11: 'Campo de Ourique'}
    return stores[store]


def increment_date(store, date_str):
    import datetime
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        after_date = str(date + datetime.timedelta(days=1))
        before_date = str(date - datetime.timedelta(days=1))

        after = get_usage(store, after_date)
        before = get_usage(store, before_date)

        return [after[0]['usage']['BIG_BALL'], before[0]['usage']['BIG_BALL']]
    except ValueError:
        return None
