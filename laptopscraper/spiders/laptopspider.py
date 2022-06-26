import scrapy


class LaptopSpider(scrapy.Spider):
    name = "laptop"
    start_urls = [
        "https://ardes.bg/laptopi/laptopi/pamet-kapatsitet-pamet-ot-16-do-16"]

    def parse(self, response):
        for products in response.css("div.product"):
            start = '<div class="isTruncated"><span>'
            end = '</span></div>'
            s = products.css("div.isTruncated").get()
            name = s[s.find(start)+len(start):s.rfind(end)]
            link = "https://ardes.bg" + products.css("a").attrib["href"]
            yield {
                "name": name,
                "price": products.css("span.price-num::text").get(),
                "link": link,
                "processor": products.css("li::text").get(),

            }
        start = '<span class="next"><a href="'
        end = '">Следваща</a>\n                                </span'
        s = response.css("span.next").get()
        np = s[s.find(start)+len(start):s.rfind(end)]
        next_page = "https://ardes.bg" + np
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
