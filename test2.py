from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.aircourts.com/').text
soup = BeautifulSoup(html_text, 'lxml')

h1 = soup.find('h1', class_ = 'insert-text hidden-xs')
text = h1.find('b').text

print(text)

