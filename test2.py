from re import I
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import requests
import datetime
import time

# selects the wanted date
chosed_day = datetime.date.today() + datetime.timedelta(days=1)

driver = Chrome(executable_path='C:\\Users\\flolivei\\Documents\\chromedriver.exe')
driver.get(f"https://www.aircourts.com/index.php/site/view_club/239/{chosed_day}/00:00")

time.sleep(2)
page_source = driver.page_source

soup = BeautifulSoup(page_source, 'lxml')

occupancy = []
courts = soup.find('div', class_ = 'club-container').find_all('div', class_ = 'court-container')
for court in courts:
  free = []
  occupied = []
  name = court.find('div', class_ = 'court-info').h3.text
  name = name.lower()
  if "padel" in name:
    free_slots = court.find('div', class_ = 'slot-container').find_all('a', onclick=True)
    for slot in free_slots:
      free.append(slot.p)
    occupied_slots = court.find('div', class_ = 'slot-container').find_all('a', onclick=False)
    for slot in occupied_slots:
      occupied.append(slot.p)
    occupancy.append({'court' : name, 'free_slots' : free, 'occ_slots' : occupied})


print(occupancy)


#html_text = requests.get('https://www.aircourts.com/').text
#soup = BeautifulSoup(html_text, 'lxml')




