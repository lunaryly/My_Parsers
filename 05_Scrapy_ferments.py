import scrapy
import time

class fermentSpider(scrapy.Spider):
    name = "FermentSpider"
    start_urls = ["https://pro-syr.ru/zakvaski-dlya-syra/mezofilnye/"]

    def parse(self, response):
        links = response.css("div.nameproduct a::attr(href)")
        for link in links:
            time.sleep(1)
            yield response.follow(link, self.parse_ferment)

        link = response.css("ul.pagination a::attr(href)")[-1].get()# достали ссылку на следующую страничку
        yield response.follow(link, self.parse)

    def parse_ferment(self, response):
        yield {
            "name": response.css("div.row h1::text").get(),
            "price": response.css("h2 span::text").get().replace(" ", "").split("руб")[0], 
            "on_sale": response.css('div.product-description b.outstock::text').get()
        }