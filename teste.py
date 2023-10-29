from datetime import datetime, timedelta

data = '2022-10-12'
new = datetime.strptime(data, '%Y-%m-%d').date()
data = '21'
new = datetime.strptime(data, '%Y-%m-%d').date()
print(new)
