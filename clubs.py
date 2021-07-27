from re import I
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
#from datetime import datetime
import requests
import datetime
import time
import unidecode
import sqlite3

driver = Chrome(executable_path='C:\\Users\\flolivei\\Documents\\chromedriver.exe')
driver.get("https://www.aircourts.com/index.php/")
location = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "location"))

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')

sports_extract = soup.find('select', id = 'sport').find_all('option', class_ = 'ac-translate')
locations_extract = soup.find('select', id = 'location').find_all('option', class_ = 'ac-translate')

for sport_extract in sports_extract:
  sport = {'code' : sport_extract['value'],
        'sport' : sport_extract.get_text()}
  print(sport)

try:
    sqliteConnection = sqlite3.connect('sports_freq.db')
    cursor = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")

    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("SQLite Database Version is: ", record)
    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")
#print(locations)

# selects the wanted date
#chosed_day = datetime.date.today() + datetime.timedelta(days=1)


#driver.get(f"https://www.aircourts.com/index.php/site/view_club/253/{chosed_day}/00:00")
