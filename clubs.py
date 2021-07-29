from re import I
from sqlite3.dbapi2 import Error
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

def create_connection(db_file):
    """ create a database connection to the SQLite database 
        specified by db_file 
    :param db_file: database file
    :retur: connection object or None
    """
    conn = None
    try: 
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    
    return conn

def create_club(conn, club):
    """ create a new club into the clubs table
    :param conn:
    :param club:
    :return: club id
    """
    sql = '''INSERT INTO club (id, name) VALUES (?, ?)'''

    cursor = conn.cursor()
    cursor.execute(sql, club)
    conn.commit()
    return cursor.lastrowid

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


database = r"C:\Users\flolivei\Documents\GitHub\auto_reservation\sports_freq.db"

# creates a database connection
conn = create_connection(database)

with conn:
    for sport_extract in sports_extract:
        club = (sport_extract["value"], sport_extract.get_text())
        id = create_club(conn, club)
        print(id)

if conn: 
    conn.close()
    print("The SQLite connection is closed")


#print(locations)

# selects the wanted date
#chosed_day = datetime.date.today() + datetime.timedelta(days=1)


#driver.get(f"https://www.aircourts.com/index.php/site/view_club/253/{chosed_day}/00:00")
