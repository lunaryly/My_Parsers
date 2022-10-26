import scrapy
import time 
 
class CoursesSpider2(scrapy.Spider):
    name = "CoursesSpider2"
    start_urls = ["https://checkroi.ru/?s=java&post_type=product",
                  "https://checkroi.ru/?s=%D0%90%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0&post_type=product",
                  "https://checkroi.ru/?s=python&post_type=product",
                  "https://checkroi.ru/?s=1c&post_type=product",
                  "https://checkroi.ru/?s=Frontend&post_type=product",
                  "https://checkroi.ru/?s=DevOps&post_type=product"]

    headers = {
      "accept": "*/*",
      "accept-encoding": "gzip, deflate, br",
      "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
      "content-length": 0,
      "content-type": "text/plain",
      "origin": "https://checkroi.ru",
      "referer": "https://checkroi.ru/",
      "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": "Windows",
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "cross-site",
      "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }
  
    def parse(self, response):        
        links = response.css("div.item_product__card a.title::attr(href)").getall()
        for link in links:
            time.sleep(1)
            # url = "https://obrazoval.ru/"
            # linkfull = url+link
            yield response.follow(link, self.parse_courses)
        link = response.css("ul.page-numbers a::attr(href)")[-1].get()# достали ссылку на следующую страничку
        yield response.follow(link, self.parse)

    def parse_courses(self, response):
        yield {
            "name": response.css("h1::text").get().replace("\xa0", " "), # название
            "school": response.css(".woocommerce-product-attributes-item.woocommerce-product-attributes-item--attribute_pa_universitet p span.val_no_link.mobfont80::text").get(), # кто обучает 
            "price": response.css("tr.attribute_row.attribute_row_skolko-stoit-obuchenie2 > td > table > tbody > tr > td > p > span::text").get().replace("\xa0", "").replace(" ", "").split("₽")[0], # цена 
            "long": response.css(".woocommerce-product-attributes-item.woocommerce-product-attributes-item--attribute_pa_prodolzhitelnost p span.val_no_link.mobfont80::text").get(), # длительность
            "skills": response.css("tr.woocommerce-product-attributes-item.woocommerce-product-attributes-item--attribute_pa_chemu-nauchites > td > p > span > a::text").getall(), # навыки
            "services": response.css("tr.woocommerce-product-attributes-item.woocommerce-product-attributes-item--attribute_pa_tehnologii > td > p > span > a::text").getall(), # Приложения и сервисы
            "difficult": response.css(".woocommerce-product-attributes-item.woocommerce-product-attributes-item--attribute_pa_uroven > td > p > span > a::text").get(), # сложность
            "content": response.css("div > ol > li::text").getall(), # Программа курса
            "rating": response.xpath('//*[@id="section-woo-rev"]/div[1]/div/span/span[1]/span/text()').get()
        }