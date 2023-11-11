from tinydb import TinyDB, Query
from datetime import date


class Production():
    def __init__(self):
        self.store = 0
        self.big_balls: int = 0
        self.small_balls: int = 0
        self.garlic_bread: int = 0
        self.date = str(date.today())

    def get_data(self):
        return {self.date:   {'big_balls': int(self.big_balls),
                              'small_balls': int(self.small_balls),
                              'garlic_bread': int(self.garlic_bread)}}


class DbConnection():
    def __init__(self, database):
        self.db: TinyDB = TinyDB(database, indent=4)
        self.data: dict = {}
        self.store = int

    def insert(self):
        self.db.table(self.store).insert(self.data)

    def update(self, date):
        self.db.table(self.store).update(
            self.data, Query().date == date)
