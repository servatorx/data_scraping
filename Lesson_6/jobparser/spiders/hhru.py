import scrapy
from scrapy.http import HtmlResponse
from Lesson_6.jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?area=&st=searchVacancy&fromSearch=true&text=python']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[contains(@class,'HH-Pager-Controls-Next')]/@href").extract_first()
        # vacansy_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href")
        vacansy_links = response.css('a.bloko-link.HH-LinkModifier::attr(href)').extract()
        for link in vacansy_links:
            yield response.follow(link,callback=self.vacansy_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacansy_parse(self, response:HtmlResponse):
        name = response.xpath('//h1/text()').extract_first()
        salary = response.xpath("//p[@class='vacancy-salary']/span/text()").extract()
        link = response.url.split("?")[0]
        yield JobparserItem(item_name=name,item_salary=salary, item_link=link)
        print(name,salary)


