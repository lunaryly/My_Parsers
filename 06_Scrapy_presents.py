import scrapy
import time

class presentSpider(scrapy.Spider):
    name = "PresentSpider"
    start_urls = ["https://siberia.eco/gotovye-podarki/"]

    def parse(self, response):
        links = response.css("a.s-product-header::attr(href)").getall()
        for link in links:
            time.sleep(1)
            url = "https://siberia.eco"
            linkfull = url+link
            yield response.follow(linkfull, self.parse_present)

    def parse_present(self, response):
        yield {
            "name": response.css('div h1::text').get(), # название
            "price": response.css("span.s-price.mr-2::text").get().replace(" ", "").split("руб")[0], # цена 
            "content": response.css("ul li a::text").getall()[1:-12] # состав
        }