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
        incremented_date = str(date + datetime.timedelta(days=store))
        return incremented_date
    except ValueError:
        return None


def create_data_to_chart_ball_usage(store, date):

    before_week = []
    big_balls = []
    small_balls = []
    for day in range(-7, 0):
        before_week.append(increment_date(day, date))

    for day in before_week:
        big_balls.append(get_usage(store, day)[0]['usage']['BIG_BALL'])
        small_balls.append(get_usage(store, day)[0]['usage']['SMALL_BALL'])

    return [before_week, [big_balls, small_balls]]


print(create_data_to_chart_ball_usage(5, '2022-05-09'))
