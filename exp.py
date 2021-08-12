import datetime

date = datetime.datetime.utcnow()
date1 = datetime.datetime.utcnow()

d = datetime.datetime(2019, 2, 4).today()
time = f'{d.hour}:{d.minute}:{d.microsecond}'
print(time)

soup = BeautifulSoup(page_source, 'lxml')
clubs = soup.find("div", class_ = "court_container").find_all("div", class_ = "club-container") # list of padel clubs in "Grande Lisboa"

for club in clubs: 
    name = club.find('div', class_ = 'club-info').h2.text
    print(name)
    print(name)ç