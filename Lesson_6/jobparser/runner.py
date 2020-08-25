from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Lesson_6.jobparser import settings
# from jobparser import settings2
from Lesson_6.jobparser.spiders.hhru import HhruSpider
from Lesson_6.jobparser.spiders.sj import SjruSpider
# from jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    #crawler_settings2 = Settings()
    #crawler_settings2.setmodule(settings)
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(SjruSpider)
    process.crawl(HhruSpider)
    process.start()