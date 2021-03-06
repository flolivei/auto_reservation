from re import I
import psycopg2
from psycopg2 import Error
#from sqlite3.dbapi2 import Error
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
#from datetime import datetime
#import requests
import datetime
import time
import unidecode
#import sqlite3
import os
import json

with open("crd.json") as f:
    data = json.load(f)

def create_connection():
    """ create a database connection to the SQLite database 
        specified by db_file 
    :param db_file: database file
    :retur: connection object or None
    """
    conn = None
    try: 
        '''
        # Connect to an existing database
        conn = psycopg2.connect(user="postgres",
                                  password="ucrsah",
                                  host="localhost",
                                  port="5432",
                                  database=db_file)
        '''
        # Connect to Heroku database
        conn = psycopg2.connect(user=data["user"],
                                  password=data["pass"],
                                  host=data["host"],
                                  port=data["port"],
                                  database=data["db"])                                  

        return conn
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    
    return conn

def sport_insert(conn, values):
    """ create a new sport into the sports table
    :param conn:
    :param sport:
    :return: sport id
    """
    sport_check = "SELECT * FROM sports WHERE code = %s AND name = %s"
    insert_sport = "INSERT INTO sports (code, name) VALUES (%s, %s)"
    
    cursor = conn.cursor()
    cursor.execute(sport_check, values)
    if not cursor.fetchall():
        cursor.execute(insert_sport, values)
    
    conn.commit()
    cursor.close()
    return cursor.lastrowid

def location_insert(conn, values):
    """ create a new sport into the sports table
    :param conn:
    :param sport:
    :return: sport id
    """
    locations_check = "SELECT * FROM locations WHERE code = %s AND name = %s"
    insert_location = "INSERT INTO locations (code, name) VALUES (%s, %s)"  
    
    cursor = conn.cursor()
    cursor.execute(locations_check, values)
    if not cursor.fetchall():
        cursor.execute(insert_location, values)

    conn.commit()
    cursor.close()
    return cursor.lastrowid

def verification_insert(conn, date):
    insert_verification = "INSERT INTO verifications (day, month, year, time) VALUES (%s, %s, %s, %s) RETURNING id"
    day = date.day
    month = date.month
    year = date.year
    time = f'{date.hour}:{date.minute}:{date.second}'
    values = (day, month, year, time)
    cursor = conn.cursor()
    cursor.execute(insert_verification, values)
    conn.commit()
    insert_id = cursor.fetchone()
    cursor.close()
    return insert_id

def sports_verification(conn, verif_id, values):
    check_sport = "SELECT id FROM sports WHERE code = %s AND name = %s"
    insert_sports_verification = "INSERT INTO sports_verif (sports_id, verif_id) VALUES (%s, %s)"

    cursor = conn.cursor()
    cursor.execute(check_sport, values)
    retrieved_list = cursor.fetchall()

    if len(retrieved_list) != 1:
        print('ERROR')
    else:
        sport_id = retrieved_list[0][0]
        ids_to_insert = (sport_id, verif_id)
        cursor = conn.cursor()
        cursor.execute(insert_sports_verification, ids_to_insert)
        
    conn.commit()
    cursor.close()
    return cursor.lastrowid

def locations_verification(conn, verif_id, values):
    check_location = "SELECT id FROM locations WHERE code = %s AND name = %s"
    insert_locations_verification = "INSERT INTO loc_verif (loc_id, verif_id) VALUES (%s, %s)"

    cursor = conn.cursor()
    cursor.execute(check_location, values)
    retrieved_list = cursor.fetchall()

    if len(retrieved_list) != 1:
        print('ERROR')
    else:
        location_id = retrieved_list[0][0]
        ids_to_insert = (location_id, verif_id)
        cursor = conn.cursor()
        cursor.execute(insert_locations_verification, ids_to_insert)
        
    conn.commit()
    cursor.close()
    return cursor.lastrowid

def call_sport_city(conn, sport, location):
    sport_select = "SELECT code FROM sports WHERE name = (%s)"
    #location_select = 'SELECT code FROM locations WHERE name = (?)'
    location_select = 'SELECT code FROM locations'

    cursor = conn.cursor()
    cursor.execute(sport_select, sport)
    retrieved_list = cursor.fetchall()
    sport_code = retrieved_list[0][0]
    cursor.execute(location_select)
    retrieved_list = cursor.fetchall()
    #location_code = retrieved_list[0][0]

    cursor.close()
    return (sport_code, retrieved_list)

def club_insert(conn, values, location_code):
    clubs_check = "SELECT * FROM clubs WHERE code = %s AND name = %s"
    insert_club = "INSERT INTO clubs (code, name, zone, location_id) VALUES (%s, %s, %s, %s)"
    sql_location_id = "SELECT id FROM locations WHERE code = (%s)"

    cursor = conn.cursor()
    cursor.execute(sql_location_id, location_code)
    retrieved_list = cursor.fetchall()
    print(type(retrieved_list))
    print(retrieved_list)
    location_id = retrieved_list[0][0]

    values = values + (location_id,)
    print(values)
    cursor.execute(clubs_check, (values[0], values[1]))
    if not cursor.fetchall():
        cursor.execute(insert_club, values)
 
    conn.commit()
    cursor.close()
    return cursor.lastrowid

def clubs_verification(conn, verif_id, values):
    check_club = "SELECT id FROM clubs WHERE code = %s AND name = %s"
    insert_clubs_verification = "INSERT INTO clubs_verif (club_id, verif_id) VALUES (%s, %s)"

    cursor = conn.cursor()
    cursor.execute(check_club, (values[0], values[1])) # values[0] = code, values[1] = name
    retrieved_list = cursor.fetchall()

    if len(retrieved_list) != 1:
        print('ERROR')
    else:
        club_id = retrieved_list[0][0]
        ids_to_insert = (club_id, verif_id)
        cursor = conn.cursor()
        cursor.execute(insert_clubs_verification, ids_to_insert)   
    conn.commit()
    cursor.close()
    return cursor.lastrowid

"""
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
"""


#driver = Chrome(executable_path='C:\\Users\\flolivei\\Documents\\chromedriver.exe')
driver = webdriver.Chrome(executable_path="C:\\Users\\flavi\\Documents\\chromedriver.exe")
driver.get("https://www.aircourts.com/index.php/")
location = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "location"))

date = datetime.datetime.utcnow()
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')

sports_extract = soup.find('select', id = 'sport').find_all('option', class_ = 'ac-translate')
locations_extract = soup.find('select', id = 'location').find_all('option', class_ = 'ac-translate')

list_code_sport = []
for sport_extract in sports_extract:
    list_code_sport.append(
        {'code' : sport_extract['value'],
        'sport' : sport_extract.get_text()}
    )
    
print(list_code_sport)

#local catabase
#database = "sports_stat"


# creates a database connection
conn = create_connection()


list_for_test = [{'code': '3', 'sport': 'T??nis'}, {'code': '1', 'sport': 'Futebol 5'}, {'code': '6', 'sport': 'Futsal'}, {'code': '2', 'sport': 'Futebol 7'}, {'code': '12', 'sport': 'Padbol'}, {'code': '14', 'sport': 'Squash'}, {'code': '8', 'sport': 'Basquetebol'}, {'code': '9', 'sport': 'Andebol'}, {'code': '10', 'sport': 'Voleibol'}, {'code': '22', 'sport': 'Teqball'}, {'code': '5', 'sport': 'Futebol 11'}, {'code': '13', 'sport': 'Bubble Football'}, {'code': '15', 'sport': 'Rugby'}, {'code': '17', 'sport': 'Futebol 5 Tabelas'}, {'code': '18', 'sport': 'Golf'}, {'code': '19', 'sport': 'T??nis de Praia'}, {'code': 
'20', 'sport': 'Pistas Atletismo'}, {'code': '21', 'sport': 'Futevolei'}, {'code': '16', 'sport': 'Salas de Desporto'}, {'code': '23', 'sport': 'Futet??nis'}, {'code': '24', 'sport': 'Nata????o'}, {'code': '25', 'sport': 'T??nis de mesa'}, {'code': '26', 'sport': 'H??quei em Patins'}, {'code': '27', 'sport': 'Patinagem art??stica'}]
with conn:

    verif_id = verification_insert(conn, date)

    for sport_extract in sports_extract:
        code = sport_extract['value']
        name = sport_extract.get_text()
        row_values = (code, name)
        sport_id = sport_insert(conn, row_values)
        sports_verification(conn, verif_id, row_values)


    for location_extract in locations_extract:
        code = location_extract['value']
        name = location_extract.get_text()
        row_values = (code, name)
        location_id = location_insert(conn, row_values)
        locations_verification(conn, verif_id, row_values)

    sport_city_ids = call_sport_city(conn, ("Padel",), ("Grande Lisboa",))
    print(sport_city_ids)

print(f"sport: {sport_city_ids[0]}")
for city in sport_city_ids[1]:
    driver.get(f"https://www.aircourts.com/site/search?sport={sport_city_ids[0]}&city={city[0]}&date=&start_time=")
    #driver.get(f"https://www.aircourts.com/site/search?sport=4&city=29&date=&start_time=")
    time.sleep(5)
    page_source = driver.page_source
    time.sleep(1)

    soup = BeautifulSoup(page_source, 'lxml')

    if soup.find('div', id = 'empty-text') is not None: #if  clubs in the c
        print(f'Cidade {city[0]}, com campos')
        clubs = soup.find('div', id = 'court_container').find_all('div', class_ = 'club-container') # list of padel clubs in "Grande Lisboa"
        #courts  soup.find('div', class_ = 'club-container').find_all('div', class_ = 'court-container')

        for club in clubs:
            code = club["data-club-id"] 
            name = club.find('div', class_ = 'club-info').h2.text
            rating = club.find("div", class_ = "rating-average").text
            rat_count = club.find("span", class_ = "rating-count").text
            zone = club.find("span", class_ = "club-zone").text
            row_values = (code, name, zone)
            location_code = (city[0],)
            club_id = club_insert(conn, row_values, location_code)
            clubs_verification(conn, verif_id, row_values)
            print(f"Name: {name}, Code: {code}, Rating: {rating}, Rating Count: {rat_count}, Zone: {zone}")         

if conn: 
    conn.close()
    print("The SQLite connection is closed")



#print(locations)

# selects the wanted date
#chosed_day = datetime.date.today() + datetime.timedelta(days=1)


#driver.get(f"https://www.aircourts.com/index.php/site/view_club/253/{chosed_day}/00:00")
