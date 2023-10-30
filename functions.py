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
        self.store = store
        self.date = date

    # def query(self, oi):
    #     result = db.search((Query().store == self.store) and
    #                        (Query().date == self.date))
    #     return result[0][f'{what you want}]

    def query(self):
        result = db.search((Query().store == self.store) &
                           (Query().date == self.date))
        return result[0]

    def get_billing(self) -> list:  # OK
        billing = self.query()

        return billing['billing']

    def get_production(self) -> list:  # OK
        production = self.query()
        return production['production']

    def get_usage(self) -> list:  # OK
        usage = self.query()
        return usage['usage']

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

    def create_data_to_ball_usage_chart(self, length, end=1):
        """receive a list to create a chart

        Args:
            length (int): how many columns to create (before days)
            example:
                length = 3 with date = 2000-01-10 will return
                    [[2000-01-09, 2000-01-08, 2000-01-07]
                    and [the usage balls of each day]]

        Returns:
            list: Will return a list with dates of day before, and usages of big and small
            balls:

        """
        if length > 0:
            end = length + 1
            length = 1
        else:
            end = 0

        before_week: list = []
        big_balls: list = []
        small_balls: list = []

        for day in range(length, end):
            before_week.append(self.increment_date(day))

        for day in before_week:
            self.date = day
            big_balls.append(self.get_usage()['BIG_BALL'])
            small_balls.append(self.get_usage()['SMALL_BALL'])

        return [before_week, [big_balls, small_balls]]
