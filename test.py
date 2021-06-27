#Simple assignment
from json import load
import time
import datetime
from selenium.webdriver import Chrome
from selenium.webdriver import support
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import re

driver = Chrome(executable_path='C:\\Users\\flolivei\\Documents\\chromedriver.exe')
driver.maximize_window()
driver.get("https://www.aircourts.com/index.php/site/login")


#assert "Python" in driver.title
email = driver.find_element_by_name("email")
email.clear()
email.send_keys("flavioliveira.7@gmail.com")
email.send_keys(Keys.RETURN)
pw = driver.find_element_by_name("password")
pw.clear()
pw.send_keys("ucrsah123")
pw.send_keys(Keys.RETURN)


#select = Select(driver.find_element_by_id('sport'))
sport = Select(driver.find_element_by_id("sport"))
#all_options = select.find_elements_by_tag_name("option")
for option in sport.options:
  #print("Value is: %s" % option.get_attribute("value"))
  option.click()


# select by visible text
sport.select_by_visible_text('Padel')

location = Select(driver.find_element_by_id('location'))

# select by visible text
location.select_by_visible_text('Grande Lisboa')

calendar = driver.find_element_by_id('datepicker')
calendar.click()

# selects the wanted date
chosed_day = datetime.date.today() + datetime.timedelta(days=1)
# selects only the day, converts to string and removes leading zeros
chosed_day = str(chosed_day.day).lstrip("0")


#x = driver.find_element(By.XPATH, '//td[text()="{}"]'.format(chosed_day))
# finds and select the day in the calendar 
x = driver.find_element_by_xpath('//td[text()="{}"]'.format(chosed_day))
#print(x.text)
x.click()

#chosed_day = int((datetime.date.today() + datetime.timedelta(days=2)).day)
#tbody = driver.find_element_by_xpath("//div[@class='datepicker-days']/table[1]/tbody[1]")
#trs = tbody.find_elements_by_tag_name("tr")
#for tr in trs:
#  days = tr.find_elements_by_tag_name("td")
#  for day in days:
    #day.find_element #print(int(day.text)) 
    #if int(day.text) == chosed_day:
    #  print("Value is: %s" % day.text) 
#    day.click() # PROBLEM
      #break
    
print("11111111111111111111")
submit = driver.find_element_by_xpath("//button[@onclick='performSearch()']")
submit.click()

# waits until timepicker input is available
timepicker = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "timepicker"))

timepicker.clear()
timepicker.send_keys("18:00")
timepicker.send_keys(Keys.RETURN)

#waits until element JS element is loaded
containers = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, "//div[@class='slot-container-v2']/a"), message='test_timeout')
time.sleep(2)
page_source = driver.page_source

soup = BeautifulSoup(page_source, 'lxml')

free_slots = {}

clubs = soup.find(id = 'court_container').find_all('div', class_ = 'club-container')
for club in clubs:
  available_times = club.table.find_all('a', onclick=True)
  if len(available_times) > 1:
    club_name = club.find(re.compile("^h")).text
    free_slots[club_name] = []
    #print(free_slots)
    for time_ in available_times:
      if time_.find("p"):
        free_slots[club_name].append({'time': time_.find('p').text, 'id': time_['id']})

print(free_slots['LX Indoor Padel'])

slot_id = 0
if free_slots['LX Indoor Padel']:
  for slot in free_slots['LX Indoor Padel']:
    if slot['time'] == "18:00":
      slot_id = slot['id']

print(slot_id)


slot = driver.find_element_by_id(slot_id)
driver.execute_script("arguments[0].click();", slot)







#
#time.sleep(4)
#court = driver.find_element_by_id("court_container")
#print(court)
#time.sleep(4)
#clubs = court.find_elements_by_class_name("club-container")
#print(len(clubs))
#i = 1
#attempts = 0#

#for club in clubs:
#  print(i)
#  exists = False
#  print(club.get_attribute("data-club-id"))
#  while attempts < 10:
#    try:
#      #apanha o slot-container-v2 mas depois n apanha o a[@class=slot] - VER O QUE SE PASSA div[@class="slot-container-v2"]
#      free_slots = club.find_element_by_xpath('.//div[@class="slot-container-v2"]')
#      exists = True
#      #print(len(free_slots))
#      print(free_slots.get_attribute('id'))
#      break
#    except:
#      attempts += 1
#      time.sleep(0.3)
#  if exists:
#    while True:
#      try:
#        print(club.get_attribute('data-club-id'))
#        i = i + 1
#        break
#      except:
#        time.sleep(0.3)

#time.sleep(2)


#cont2 = driver.find_elements_by_xpath("//div[@class='club-container']")
#print(len(clubs))
#print(len(cont2))

#containers = WebDriverWait(driver, 10).until(lambda x: x.find_elements(By.CLASS_NAME, "club-container"), message='test_timeout')
#print(len(containers))

#available_time = WebDriverWait(driver, 10).until(lambda x: x.find_elements(By.XPATH, "//a[@class='slot']/p[text()='18:00']"), message='test_timeout')
#print(len(available_time))


#available_time2 = WebDriverWait(driver, 10).until(lambda x: x.find_elements(By.XPATH, "//div[@class='visible-xs small-container']/div[@class='club-info']/div[@class='slot-container-v2']/a[@class='slot']/p[text()='18:00']"), message='test_timeout')
#print(len(available_time2))


  



#t = driver.find_element_by_xpath("//div[div[@class='visible-xs small-container']/div[@class='club-info']/div[@class='slot-container-v2']/a[@class='slot']/p[text()='18:00']]")
#print(t.get_attribute('data-club-id'))


# select by visible text

#driver.close()