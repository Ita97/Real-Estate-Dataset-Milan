import scrapy

DOWNLOAD_DELAY = 0.5 # 500 ms of delay between each request

# Item to store all the field of interest
class CasaItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    mq = scrapy.Field()
    rooms = scrapy.Field()
    address = scrapy.Field()
    bathrooms = scrapy.Field()
    ec = scrapy.Field()


class CasaSpider(scrapy.Spider):
    name = 'casa'
    city = 'milano' # change to obtain dataset from different cities in Italy
    allowed_domains = ['www.casa.it']
    start_urls = ['https://www.casa.it/vendita/residenziale/'+city+'/']

    # scrape each page
    def start_requests(self):
	end_page = 8 # last page to scrape
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        url = self.start_urls[0]
        for page in range(1, end_page):
            yield scrapy.Request(url+"?page="+str(page), headers=headers)

    def parse(self, response):
        for house in response.css("div article.srp-card"):
            item = CasaItem()
            price = house.css('div.info-features__price p.c-txt--f0::text').extract()
            if len(price):
                price = price[1]
            else:
                continue

            mq = house.css('div.info-features__dtls div.grid--gutters-l div.info-features__item::text').extract()[0]
            locali = house.css('div.info-features__dtls div.grid--gutters-l div.info-features__item::text').extract()[2]
            next_page = house.css('div.csa_gallery__slide figure.is-full-fit a').xpath('@href').extract_first()
            item["mq"] = mq
            item["rooms"] = locali
            item["price"] = price
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

            yield response.follow(next_page, callback=self.parse_house_page, headers=headers, cb_kwargs=dict(item=item))

    def parse_house_page(self, house, item):

        title = house.css('div.layout__info-spacing div.infos_container div.infos *.infos__H1::text').extract_first()
        char = house.css('div.layout__info-spacing div.chars__feats ul li ::text').extract()
        bagni = char[char.index("Bagni")+2]
        energia = house.css('div.chars__ec__class span.chars__ec__class--value::text').extract_first()
        addr = house.css('div.layout__info-spacing div.layout div.map div.grid p.map__head--addrs::text').extract_first()
        item["title"] = title
        item["bathrooms"] = bagni
        item["address"] = addr
        item["ec"] = energia

        yield item


