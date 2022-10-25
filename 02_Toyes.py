import requests
import bs4
from bs4 import BeautifulSoup
import lxml
import html.parser
import html5lib
import csv
import re
import time

URL = 'https://tomsk.richfamily.ru/catalog/igrushki/myagkie/?PAGEN_1={}'

def get_html(page):  
  session = requests.session()
  session.headers = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
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

def get_toy_info(item):
  """ Собирает информацию о игрушке """ 
  title = item.select_one("div.kkb_content-item__name-brand")
  if not title:
    print("Error find title!")
    return
  
  title = title.text.split("\n")[1].replace("cм ", "см ").split("см ")[0]  
  clear_title = re.split('\d',title)[0]
  p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
  size = re.search(p, title)[0]  
  price = item.select_one("div.kkb_content-item__price-box")
  if not price:
    print("Error find price!")
    return
  price = price.text.replace(" ", "").split("\n")[2].split("\t")[14]

  # Возвращаем информацию об игрушке
  return {
      "title": clear_title,
      "price": price,
      "size": size      
  }

def get_toyes_info(soup):
  """ Информация об игрушках на странице """  
  list_rows = soup.select_one("div.kkb_catalog-content-main ")   
  all_items = list_rows.select("div.kkb_content-item")
  result = []

  for item in all_items:
    result.append(get_toy_info(item))
  # Краткая запись
  # result = [get_toy_info(li) for li in all_li]
  return result

result = []
page = 1
while page != 17:
  # Перерыв между запросами
  time.sleep(3)
  soup = get_soup(page)
  print(page)
  if not soup:
    # Если нету супа, то выходим из цикла => либо ошибка, либо конец страниц
    break
  # Получаем информацию об игрушках
  toyes_info = get_toyes_info(soup)
  # Записываем в result получившуюся инфу об игрушках на странице
  result = result + toyes_info
  
  page = page + 1
print(f"Всего пройдено страниц: {page-1}")

with open("toyes.csv", "w") as f:
  writer = csv.DictWriter(f, result[0].keys())
  writer.writeheader()
  for t in result:
    writer.writerow(t)
