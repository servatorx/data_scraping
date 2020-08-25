import scrapy
from scrapy.http import HtmlResponse
from Lesson_6.jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sj'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[contains(@class,'f-test-link-Dalshe')]/@href").extract_first()
        vacansy_links = response.xpath("//div[@class='_3mfro PlM3e _2JVkc _3LJqf']/a/@href")
        #vacansy_links = response.css('a.bloko-link.HH-LinkModifier::attr(href)').extract()
        for link in vacansy_links:
            yield response.follow(link,callback=self.vacansy_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacansy_parse(self, response:HtmlResponse):
        name = response.xpath('//h1/text()').extract_first()
        salary = response.xpath("//span[@class='_3mfro _2Wp8I PlM3e _2JVkc']/text()").extract()
        link = response.url
        yield JobparserItem(item_name=name,min_salary=salary, item_link=link)
        print(name,salary,link)


