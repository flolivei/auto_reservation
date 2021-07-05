from re import I
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
#from datetime import datetime
import requests
import datetime
import time

# selects the wanted date
chosed_day = datetime.date.today() + datetime.timedelta(days=1)

driver = Chrome(executable_path='C:\\Users\\flolivei\\Documents\\chromedriver.exe')
driver.get(f"https://www.aircourts.com/index.php/site/view_club/239/{chosed_day}/00:00")

time.sleep(3)
page_source = driver.page_source
time.sleep(1)

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
      try:
        if slot.p.text:
          free.append(slot.p.text)
      except:
        free.append("none")
    occupied_slots = court.find('div', class_ = 'slot-container').find_all('a', onclick=False)
    previous_slot = '00:00'
    for slot in occupied_slots:
      try:
        if slot.p.text:
          occupied.append(slot.p.text)
      except:
        occupied.append('none')
    occupancy.append({'court' : name, 'free_slots' : free, 'occ_slots' : occupied})

for i in occupancy:
  for index, slot in enumerate(i['free_slots']):
    if slot == 'none':
      print(f'Index: {index}')
      print(f'Index - 1: {index-1}')
      time_for_none = datetime.datetime.strptime(i['free_slots'][index-1],'%H:%M') #falta acresecentar 30min
      #i['free_slot'][index-1]
      print(time_for_none)
      #i['free_slot'][index] = time_for_none




print(occupancy)


#html_text = requests.get('https://www.aircourts.com/').text
#soup = BeautifulSoup(html_text, 'lxml')




