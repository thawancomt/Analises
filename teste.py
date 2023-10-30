from datetime import datetime, timedelta


class cao():
    def __init__(self, cor, pelo):
        self.cor = cor
        self.pelo = pelo

    def exibircore(self):
        return self.cor


cao1 = cao('preto', False)
cao1 = cao('branco', False)

print(cao1.exibircore())
