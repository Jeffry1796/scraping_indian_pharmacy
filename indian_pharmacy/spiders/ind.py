import scrapy
import requests

class school_scrape(scrapy.Spider):
    name = 'ind_med'

    url = 'https://pharmeasy.in/health-care/'

    header={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    }

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.header, callback=self.parse)

    def parse(self, response):
        for each_url in response.xpath("//div[@class='_38ewW']/a/@href").extract():
            cd_prodcut = each_url.split('-')[-1]
            for x in range (1,100):
                api_product = 'https://pharmeasy.in/api/otc/getCategoryProducts?categoryId='+cd_prodcut+'&page='+str(x)
                req_api = requests.get(url = api_product, headers = self.header)
                product_data = req_api.json()
                if len(product_data['data']['products']) == 0:
                    break
                else:
                    for ttl_prod in range (len(product_data['data']['products'])):
                        yield {
                            'Category': each_url.split('/')[-1],
                            'ID': product_data['data']['products'][ttl_prod]['productId'],
                            'Name': product_data['data']['products'][ttl_prod]['name'],
                            'Manufacturer': product_data['data']['products'][ttl_prod]['manufacturer'],
                            'Price': product_data['data']['products'][ttl_prod]['salePriceDecimal']
                        }
