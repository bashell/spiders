# -*- coding: utf-8 -*-

import scrapy
from weather.items import WeatherItem


class WeatherSpider(scrapy.Spider):
    name = "myweather"
    allowed_domains = ["sina.com.cn"]
    start_urls = ['http://weather.sina.com.cn']

    def parse(self, response):
        item = WeatherItem()
        item['city'] = response.xpath('//*[@id="slider_ct_name"]/text()').extract()
        futureTenDay = response.xpath('//*[@id="blk_fc_c0_scroll"]')
        item['date'] = futureTenDay.css('p.wt_fc_c0_i_date::text').extract()
        item['dayDesc'] = futureTenDay.css('img.icons0_wt::attr(title)').extract()
        item['dayTemp'] = futureTenDay.css('p.wt_fc_c0_i_temp::text').extract()

        return item
