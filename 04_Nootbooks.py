from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path='/usr/lib/chromium-browser/chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
  driver.get("https://www.nbcomputers.ru/catalog/noutbuki/")
  driver.implicitly_wait(10)
  el = driver.find_element(By.CSS_SELECTOR,'#catalog-listing > button')
  actions = ActionChains(driver)
  actions.move_to_element(el).click().perform()

  wait = WebDriverWait(driver, timeout=10)
  
  while True:    
    actions.move_to_element(el).perform()
    wait.until(EC.element_to_be_clickable(el)).click()

except Exception as ex:
  print(f'Error: {ex}')

html = driver.page_source

driver.quit()

soup = BeautifulSoup(html, "html.parser")

# Название ноутбука * Цена ноутбука * Код товара
catalog = soup.select_one("div.CatalogGridstyles__CatalogGrid__Inner-sc-bla7rq-1")
nootbooks = catalog.select("article")

nootbook_list = []
for noot in nootbooks:
  name = noot.select_one("a h2").text
  price = noot.select_one("div.CatalogItem_Rectanglestyles__CatalogItemRectangle__PriceAndButtons-sc-ep8kec-3 span").text.replace("\xa0", "")[:-1]
  code = noot.select_one("span p").text.split()[1]  
  nootbook_list.append({
      "code": code,
      "name": name,
      "price": price      
  })

with open("nootbooks.csv", "w") as f:
  writer = csv.DictWriter(f, nootbook_list[0].keys())
  writer.writeheader()
  for r in nootbook_list:
    writer.writerow(r)