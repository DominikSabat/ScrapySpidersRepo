import scrapy
from datetime import datetime, timedelta


class SecondPrisonSpider(scrapy.Spider):
    name = "SecondPrison"
    start_urls = ["https://netweb.netdatacorp.net/NDLEC/bok/cgibokcole.html"]
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'
    }
    date = str((datetime.now() - timedelta(days=7)).strftime("%m/%d/%Y"))

    def parse(self, response):
        # inspect_response(response, self)

        yield scrapy.FormRequest.from_response(response, formdata= {
            "S109ASOFDT": self.date,
            "S109INMNAM": "a",
        }, callback=self.parseForm)

    def parseForm(self, response):
        # inspect_response(response, self)

        for i in range(len(response.css("L01-KEY::text"))):
            data = {
                "S101KEY": response.css("L01-KEY::text")[i].get(),
                "S101LIB": "DATACOLE",
                "S101PFX": "LE",
                "S101CNTY": "Coleman",
                "S101COCOD": "COLEM",
            }
            yield scrapy.FormRequest(url="https://netweb.netdatacorp.net/NDLEC/bok/CGIBOK101.ws", formdata=data,method='POST',
                                     callback=self.parsePrisonser)

        next_page = {
            "S109ORD": "NX",
            "109ASOFDT": self.date,
            "S109INMNAM": response.css("L01-INMATE-NAME::text")[-1].get(),
            "S109KEY": response.css("L01-KEY::text")[-1].get(),
            "S109LIB": "DATACOLE",
            "S109PFX": "LE",
            "S109CNTY": "Coleman",
            "S109COCOD": "COLEM",
        }

        yield scrapy.FormRequest(url="https://netweb.netdatacorp.net/NDLEC/bok/CGIBOK109.ws", formdata=next_page,method='POST',
                                 callback=self.parseNextPage)


    def parseNextPage(self, response):
        # inspect_response(response, self)


        for i in range(len(response.css("L01-KEY::text"))):
            inmates_data = {
                "S101KEY": response.css("L01-KEY::text")[i].get(),
                "S101LIB": "DATACOLE",
                "S101PFX": "LE",
                "S101CNTY": "Coleman",
                "S101COCOD": "COLEM",
            }
            yield scrapy.FormRequest(url="https://netweb.netdatacorp.net/NDLEC/bok/CGIBOK101.ws", formdata=inmates_data,method='POST',
                                     callback=self.parsePrisonser)

    def parsePrisonser(self, response):
        # inspect_response(response, self)

        yield {
            'Booking Number': response.css("L02-ITEM1::text")[1].get().replace(" ", ""),
            'Full Name': response.css("L02-ITEM1::text")[2].get(),
            'Race': response.css("L04-ITEM1::text")[0].get().replace(" ", ""),
            'Ethnic': response.css("L04-ITEM2::text")[0].get(),
            'Gender': response.css("L04-ITEM3::text")[0].get(),
            'Age': response.css("L04-ITEM4::text")[0].get(),
            'Charges': response.css("L27-CHARGE::text").getall(),
            'Bond': response.css("L27-BOND-AMT::text").getall(),
            'Booking Date': response.css("L27-BOOKIN-DATE::text").getall(),
        }



