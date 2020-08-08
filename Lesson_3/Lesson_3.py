from pymongo import MongoClient
import pandas as pd
import re
from hh_sj import find_vac


def add_new_vac(vac_list):
    i = 0
    for vac in vac_list:
        if vac_db.count_documents({"_id": vac["_id"]}) == 0:
            vac_db.insert_one(vac)
            i += 1
    print(f"Добавлено {i} вакансий")


def find_salary(salary):
    vac_gt = vac_db.find({'$or': [{'salary_min': {'$gt': salary }}, {'salary_max': {'$gt': salary}}]})
    list_cur = list(vac_gt)
    return list_cur




vacations = find_vac()
#df = pd.DataFrame(vacations)
#print(df.to_string())
#print(vacations)

client = MongoClient('127.0.0.1',27017)
db = client['users_db']

vac_db = db.vacations
#vac_db.delete_many({})
add_new_vac(vacations)

sal = int(input("Введите зарплату для поиска: "))
df = pd.DataFrame(find_salary(sal))
print(df.to_string())
