import requests
import bs4
from bs4 import BeautifulSoup
import lxml
import html.parser
import html5lib
import csv
import re
import time

URL = 'http://ru-pets.ru/index.php?m=6&to=1&c=2&page={}'

def get_html(page):  
  session = requests.session()
  session.headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
      "Accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
  }

  try:   
    res = session.get(URL.format(page))
    res.raise_for_status()
  except Exception as ex:
    print(ex)
    return
  return res.text

def get_soup(page):    
  html = get_html(page) 
  if not html: return  
  soup = BeautifulSoup(html, "lxml")
  return soup


def get_show_info(item):
  """ Собирает информацию о выставке """ 
  date = item.select_one('h2').text.split(",")[0] # Дата проведения
  if not date:
    date = ""
    return

  title = item.select_one('h2 span').text # Название выставки
  if not title:
    title = ""
    return

  texts = [i.text if i.text != "" else "нет" for i in item.select('div.msgtext')][0] # Клуб-Организатор
  if "Клуб - Организатор:" not in texts:
    club = "нет"
  else:
    club = texts.split("Клуб - Организатор: ")[1].split(";")[0]

  # Возвращаем информацию о выставке
  return {
      "date":date,
      "title": title,
      "club": club      
  }

def get_shows_info(soup):
  """ Информация о выставках на странице """
  # 
  list_rows = soup.select_one("#inner")
  # Получаем карточки
  all_items = list_rows.select("'div.listitem'")
  result = []
  # Проходимся по каждой карточке и достаем из нее информацию
  for item in all_items:
    result.append(get_show_info(item))
  # Краткая запись
  # result = [get_show_info(li) for item in all_items]
  return result

result = []
page = 1
while page != 78:
  # Перерыв между запросами
  time.sleep(3)
  soup = get_soup(page)
  print(page)
  if not soup:
    # Если нету супа, то выходим из цикла => либо ошибка, либо конец страниц
    break
  # Получаем информацию о выставках
  shows_info = get_shows_info(soup)
  # Записываем в result получившуюся инфу о выставках на странице
  result = result + shows_info
  
  page = page + 1
print(f"Всего пройдено страниц: {page-1}")

with open("shows.csv", "w") as f:
  writer = csv.DictWriter(f, result[0].keys())
  writer.writeheader()
  for t in result:
    writer.writerow(t)