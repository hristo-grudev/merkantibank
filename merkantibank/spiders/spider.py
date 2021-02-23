import scrapy
from scrapy.exceptions import CloseSpider

from scrapy.loader import ItemLoader
from ..items import MerkantibankItem
from itemloaders.processors import TakeFirst


class MerkantibankSpider(scrapy.Spider):
	name = 'merkantibank'
	start_urls = ['http://www.merkantibank.com/English/corporate/news/2016/default.aspx']
	page = 2016

	def parse(self, response):
		post_links = response.xpath('//a[@class="ModuleHeadlineLink"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		self.page += 1
		next_page = f'http://www.merkantibank.com/English/corporate/news/{self.page}/default.aspx'

		if not post_links:
			raise CloseSpider('no more pages')

		yield response.follow(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1[@class="ModuleTitle ModuleDetailHeadline"]//text()').get()
		description = response.xpath('//div[@class="xn-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="ModuleDate"]/text()').get()

		item = ItemLoader(item=MerkantibankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
