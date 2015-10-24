import scrapy

class MySpider(scrapy.Spider):
  name='cubespider'
  allowed_domains=["lightake.com"]
  start_urls=['http://www.lightake.com/c/Puzzles-Magic-Cube_001?page=1&pagesize=16&sort=0&showtype=0&startprice=0&endprice=0']

  def parsecube(self,response):
    name=response.xpath('//h3[@class="mb10 f16"]/text()').extract()[0].strip()  
    sku=response.xpath('//div[@id="_productId"]/text()').extract()[0].strip()
    price=response.xpath('//span[@class="dtl_price"]/text()').extract()[0].strip()
    cubetype=response.xpath('//a[@class="vm"][3]/text()').extract()[0].strip()
    yield {'sku':sku, 'name':name, 'price':price, 'type':cubetype}

  def parse(self,response):
    cubes=response.xpath('//span[@class="ovh_2line mt5"]/a[@target="_blank"]/@href').extract()
    for cube in cubes:
      cubeurl=response.urljoin(cube)
      yield scrapy.Request(cubeurl,callback=self.parsecube)
    
    nexturl=response.xpath('//a[@class="inline_any page_simp"]/@href').extract()
    if nexturl: nexturl=response.urljoin(nexturl[0])
    yield scrapy.Request(nexturl, callback=self.parse)
