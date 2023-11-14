from tinydb import TinyDB, Query
from datetime import date

store_dict = {
    3: 'Colombo',
    5: 'Odivelas',
    11: 'Campo de Ourique',
    13: 'Coina',
    25: 'Baixa Chiado'
}


class Production():
    def __init__(self):
        self.store = 0
        self.big_balls: int = 0
        self.small_balls: int = 0
        self.garlic_bread: int = 0
        self.date = str(date.today())
        self.articles = ['big_balls', 'small_balls', 'garlic_bread']

    def get_data(self):
        return {'date': self.date,
                'big_balls': int(self.big_balls),
                'small_balls': int(self.small_balls),
                'garlic_bread': int(self.garlic_bread)}


class DbConnection():
    def __init__(self, database):
        self.db: TinyDB = TinyDB(database, indent=4)
        self.data: dict = {}
        self.store = int

    def insert(self):
        self.db.table(store_dict[self.store]).insert(self.data)

    def update(self, date):
        self.db.table(self.store).update(
            self.data, Query().date == date)

    def get_data(self, date=None):
        try:
            store = int(self.store)
            data = self.db.table(store_dict[store])
            search_result = data.search(Query().date == date)

            if not search_result:
                raise IndexError
            else:
                return search_result

        except IndexError:
            return [{'big_balls': 0, 'small_balls': 0, 'garlic_bread': 0}]


teste = DbConnection('teste.json')
teste.store = 3
print(teste.get_data('2023-11-13'))
