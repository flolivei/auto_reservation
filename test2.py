from re import I
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
#from datetime import datetime
import requests
import datetime
import time
import unidecode

# selects the wanted date
chosed_day = datetime.date.today() + datetime.timedelta(days=1)

driver = Chrome(executable_path='C:\\Users\\flolivei\\Documents\\chromedriver.exe')
driver.get(f"https://www.aircourts.com/index.php/site/view_club/253/{chosed_day}/00:00")

time.sleep(3)
page_source = driver.page_source
time.sleep(1)

soup = BeautifulSoup(page_source, 'lxml')

occupancy = []
courts = soup.find('div', class_ = 'club-container').find_all('div', class_ = 'court-container')
#list for padel courts. 
padel_courts = []
for court in courts:
  free = []
  occupied = []
  #finds court name and lower case it
  name = court.find('div', class_ = 'court-info').h3.text.lower()
  name = unidecode.unidecode(name) #removes accents with regular characters without accents
  #list for slot and status. Will contain dictionaries
  slot_status_pair = []
  #finds courts with "padel" in the name, then finds all the slots
  if "tenis" not in name:
    all_slots = court.find('div', class_ = 'slot-container').find_all('a')
    #for each slot, checks for "onclick" attribute
    for index, slot in enumerate(all_slots):
      if 'onclick' in slot.attrs:
        try:  #if onclick attribute tries to find text in child p
          if slot.p.text:
            slot_status_pair.append({'time' : slot.p.text, 'status' : 'free'})  # if child p with text, appends a dictionary with time and status of that slot
        except: #if there's no text in child p, appends a dictionary with "none" for the time
          slot_status_pair.append({'time' : 'none', 'status' : 'free'}) #TODO try to add time to none at this stage by going to previous index
      else: #if there's no "onclick" attribute means that the slot is occupied 
        slot_status_pair.append({'time' : slot.p.text, 'status' : 'occupied'}) #appends a dictionary for the occupied
    padel_courts.append({'name' : name, 'schedule' : slot_status_pair}) # appends another court with it's schedule to the initial list of courts

#print(padel_courts)

for court in padel_courts:
  for index, slot in enumerate(court['schedule']):
    if slot['time'] == 'none':
      if index == 0:
        time_for_none = datetime.datetime.strptime(court['schedule'][index+1]['time'],'%H:%M') - datetime.timedelta(minutes=30)  
        slot['time'] = time_for_none.strftime("%H:%M")
      else: 
        time_for_none = datetime.datetime.strptime(court['schedule'][index-1]['time'],'%H:%M') + datetime.timedelta(minutes=30)  
        slot['time'] = time_for_none.strftime("%H:%M")

for court in padel_courts:
  print_name = True
  for slot in court['schedule']:
    if slot['status'] == 'free':
      if print_name:
        print(court['name'])
        print_name = False
      print(f'Free: {slot["time"]}')

"""    free_slots = court.find('div', class_ = 'slot-container').find_all('a', onclick=True)
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

print(occupancy)

for i in occupancy:
  for index, slot in enumerate(i['free_slots']):
    if slot == 'none':
      time_for_none = datetime.datetime.strptime(i['free_slots'][index-1],'%H:%M') + datetime.timedelta(minutes=30)  #falta acresecentar 30min
      i['free_slots'][index] = time_for_none.strftime("%H:%M")
      #considerar funcao recursiva 
      #i['free_slot'][index-1]
      #i['free_slot'][index] = time_for_none






print(occupancy)"""


#html_text = requests.get('https://www.aircourts.com/').text
#soup = BeautifulSoup(html_text, 'lxml')




