# -*- coding: utf-8 -*-
import re
from scrapy import Spider, Request, FormRequest
from weibo.items import WeiboItem


class SearchSpider(Spider):
    name = "search"
    allowed_domains = ["weibo.cn"]
    start_urls = [
        "https://weibo.cn/eauthermaleavene",
"https://weibo.cn/acquadiparma",
"https://weibo.cn/AlfredDunhill",
"https://weibo.cn/AmorepacificHongKong",
"https://weibo.cn/annasuicosmetics",
"https://weibo.cn/artistry",
"https://weibo.cn/vaupres",
"https://weibo.cn/avenedermatologist",
"https://weibo.cn/avonvoices",
"https://weibo.cn/benefit",
"https://weibo.cn/biotherm",
"https://weibo.cn/bobbibrownchina",
"https://weibo.cn/bulgari",
"https://weibo.cn/burberry",
"https://weibo.cn/ckBeauty",
"https://weibo.cn/52carslan",
"https://weibo.cn/chcedo",
"https://weibo.cn/chanel",
"https://weibo.cn/cijiws",
"https://weibo.cn/chloeparis",
"https://weibo.cn/clarins",
"https://weibo.cn/clarisonicchina",
"https://weibo.cn/CledepeauBeaute",
"https://weibo.cn/cliniqueu",
"https://weibo.cn/dabaohuodong",
"https://weibo.cn/dhcsh",
"https://weibo.cn/dior",
"https://weibo.cn/elizabetharden",
"https://weibo.cn/esteelauder",
"https://weibo.cn/etudehousechina",
"https://weibo.cn/freshBeauty",
"https://weibo.cn/gf1992",
"https://weibo.cn/giorgioarmaniBeauty",
"https://weibo.cn/parfumsgivenchy",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_Maxpage)

    def parse_Maxpage(self, response):
        values = response.xpath('//*[@id="pagelist"]/form/div/input[1]/@value').extract_first()
        print("共有",values,"页")
        for page in range(int(values) + 1):
            starturl = '{url}?page={page}'.format(url=response.url, page=page)
            yield Request(starturl, callback=self.parse_index)


    def parse_index(self, response):
        weibos = response.xpath('//div[@class="c" and contains(@id, "M_")]')
        print(len(weibos), weibos)
        for weibo in weibos:
            is_forward = bool(weibo.xpath('.//span[@class="cmt"]').extract_first())
            if is_forward:
                detail_url = weibo.xpath('.//a[contains(., "原文评论[")]//@href').extract_first()
            else:
                detail_url = weibo.xpath('(.//a[contains(., "评论[")]/@href)').extract_first()
            yield Request(detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        url = response.url
        content = ''.join(response.xpath('//div[@id="M_"]//span[@class="ctt"]//text()').extract())
        id = re.search('comment\/(.*?)\?', response.url).group(1)
        comment_count = response.xpath('//span[@class="pms"]//text()').re_first('评论\[(.*?)\]')
        forward_count = response.xpath('//a[contains(., "转发[")]//text()').re_first('转发\[(.*?)\]')
        like_count = response.xpath('//a[contains(., "赞[")]//text()').re_first('赞\[(.*?)\]')
        posted_at = response.xpath('//div[@id="M_"]//span[@class="ct"]//text()').extract_first(default=None)
        user = response.xpath('//div[@id="M_"]/div[1]/a/text()').extract_first()
        weibo_item = WeiboItem()
        for field in weibo_item.fields:
            try:
                weibo_item[field] = eval(field)
            except NameError:
                print('Field is Not Defined', field)
        yield weibo_item
