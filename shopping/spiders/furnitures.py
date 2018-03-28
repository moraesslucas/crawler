# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from shopping.items import ShoppingItem

class FurnituresSpider(CrawlSpider):
    name = 'furnitures'
    allowed_domains = ['www.buscape.com.br']
    start_urls = ['http://www.buscape.com.br/search/iphone']

    rules = (
            Rule(
                LinkExtractor(
                    allow=(),
                    restrict_css=(
                        '.bui-pagination--link',
                    )
                ),
                callback='parse_item',
                follow=True
            ),
        )

    def parse_item(self, response):
        print('Processando..'+response.url)
        items = response.css('.bui-price > .bui-product__link').extract()
        products = ShoppingItem()
        for span in items:
            attr = BeautifulSoup(span).find('a').attrs
            products['nome'] = attr['data-galabel']
            products['preco'] = attr['data-preco']
            products['url'] = attr['href']
            yield products
