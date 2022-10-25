import requests
import bs4
from bs4 import BeautifulSoup
import lxml
import html.parser
import html5lib
import csv
import re
import time

URL = "http://www.gctc.ru/main.php?id=98.1"

def get_html(URL):  
  session = requests.session()
  session.headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
      "Accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
  }

  try:   
    res = session.get(URL)
    res.raise_for_status()
  except Exception as ex:
    print(ex)
    return
  return res.text

def get_soup(URL):
  html = get_html(URL)
  if not html: return
  soup = BeautifulSoup(html, "lxml")
  return soup

soup = get_soup(URL)
li = soup.select_one("div.ie_infoh")

data = []
for element in li:
  if type(element) is not bs4.element.NavigableString:
    s = {}
    if element.name == 'h1':
      date = element.text[:2]
      mounth = element.text[2:]      
    else:
      if element.select_one("div.news"):
        year = element.text.split('\n')[1][:4]        
        ivent = element.text.split('\n')[2]
        dates = date + ' ' + mounth + ' ' + year
        s = {
            'date': dates,
            'ivent': ivent    
        }
        data.append(s)      

with open("dates.csv", "w") as f:
  writer = csv.DictWriter(f, data[0].keys())
  writer.writeheader()
  for r in data:
    writer.writerow(r)
