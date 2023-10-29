"""Some methods needs conection with the modules imported from main"""
from tinydb import Query, TinyDB

db = TinyDB('databases/dados.json')

store_dict = {
    3: 'Colombo',
    5: 'Odivelas',
    11: 'Campo de Ourique',
    13: 'Coina',
    25: 'Baixa Chiado'
}


class StoreAnalysis():

    def __init__(self, store: int, date: str):
        self.date = date
        self.store = store

    def get_billing(self) -> list:  # OK
        billing = db.search(
            (Query().store == self.store) &
            (Query().date == self.date)
        )
        return billing

    def get_production(self) -> list:  # OK
        production = db.search(
            (Query().store == self.store) &
            (Query().date == self.date)
        )
        return production

    def get_usage(self) -> list:  # OK
        usage = db.search(
            (Query().store == self.store) &
            (Query().date == self.date)
        )
        return usage

    def define_store(self) -> str:  # OK
        return store_dict[self.store]

    def increment_date(self, day: int) -> str:  # OK
        from datetime import datetime, timedelta

        try:
            date = datetime.strptime(self.date, '%Y-%m-%d').date()

            incremented_date = str(date + timedelta(days=day))

            return incremented_date

        except ValueError:
            raise ('Invalid date')

    def create_data_to_ball_usage_chart(self, length):  # OK

        before_week: list = []
        big_balls: list = []
        small_balls: list = []

        for day in range(length, 0):
            before_week.append(self.increment_date(day))

        for day in before_week:
            self.date = day
            big_balls.append(self.get_usage()
                             [0]['usage']['BIG_BALL'])
            small_balls.append(self.get_usage()
                               [0]['usage']['SMALL_BALL'])

        return [before_week, [big_balls, small_balls]]
