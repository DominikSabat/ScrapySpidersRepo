import scrapy


class QuotesSpider(scrapy.Spider):
    name = "Prison"
    start_urls = [
        'http://www.adamscosheriff.org/inmate-roster/?per_page=100',
    ]

    def parse(self, response):
        yield from response.follow_all(css="div.inmate-info a::attr(href)", callback=self.parsePrisoner)

        next_page = response.css("div.nav-links a.next::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parsePrisoner(self, response):
        yield {
            'Full Name': response.css("div.inmate-info p::text").extract()[0],
            'Booking Number': response.css("div.inmate-info p::text").extract()[1],
            'Age': response.css("div.inmate-info p::text").extract()[2],
            'Gender': response.css("div.inmate-info p::text").extract()[3],
            'Race': response.css("div.inmate-info p::text").extract()[4],
            'Addres': response.css("div.inmate-info p::text").extract()[5],
            'Booking Date': response.css("div.inmate-info p::text").extract()[7],
            'Charges': response.css("div.inmate-info p::text").extract()[8],
            'Bond': response.css("div.inmate-info p::text").extract()[9],
        }