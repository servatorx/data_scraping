# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.vacansy


    def process_item(self, item, spider):
        #collection = self.mongo_base[spider.name]
        collection = self.mongo_base["vacs"]
        print("*"*50)
        salary = item['item_salary']
        if spider.name == 'hhru':
            item['site'] = "HH"
            item['min_salary'], item['max_salary'], item['cur'] = self.hh_process_salary(salary)
        else:
            item['site'] = "SJ"
            item['min_salary'], item['max_salary'], item['cur'] = self.sj_process_salary(salary)



        collection.insert_one(item)

        return item

    def hh_process_salary(self, salary):
        if len(salary) == 7:
            min_salary = salary[1]
            max_salary = salary[3]
            cur = salary[5]
        elif len(salary) == 5:
            if salary[0].startswith("от"):
                min_salary = salary[1]
                max_salary = None
                cur = salary[3]
            else:
                min_salary = None
                max_salary = salary[1]
                cur = salary[3]
        else:
            min_salary, max_salary, cur = None,None,None

        return min_salary, max_salary, cur

    def sj_process_salary(self, salary):
        if salary[0].startswith("По договорённости"):
            min_salary, max_salary, cur = None, None, None
            return min_salary, max_salary, cur

        if len(salary) == 4:
            min_salary = salary[0]
            max_salary = salary[1]
            cur = salary[3]
        elif len(salary) == 3:
            if salary[0].startswith("от"):
                min_salary = salary[2][:-3]
                max_salary = None
                cur = salary[2][-3:]
            else:
                min_salary = None
                max_salary = salary[2][:-3]
                cur = salary[2][-3:]
        else:
            min_salary, max_salary, cur = None, None, None

        return min_salary, max_salary, cur


