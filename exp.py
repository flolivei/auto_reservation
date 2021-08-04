import datetime

date = datetime.datetime.utcnow()
date1 = datetime.datetime.utcnow()

d = datetime.datetime(2019, 2, 4).today()
time = f'{d.hour}:{d.minute}:{d.microsecond}'
print(time)