from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd
import re


def get_soup(link, params):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    response = requests.get(link, headers=headers, params=params)
    soup = bs(response.text, 'lxml')
    return soup

def check_hh_pages(soup):
    if soup.find('div', {'data-qa': 'pager-block'}) == None:

        max_page = 1
    else:

        tt= soup.find('a', {'class': 'HH-Pager-Controls-Next'}).previousSibling
        if len(tt.getText().strip()) == 0:
            max_page = len(soup.find('div', {'data-qa': 'pager-block'}).find('span', {'bloko-button-group'}))
        else:
            max_page = tt.find('a', {'class': 'bloko-button HH-Pager-Control'}).getText()
    return int(max_page)


def check_sj_pages(soup):
    if soup.find('div', {'class': '_3zucV L1p51 undefined _2guZ- _GJem'}) == None:
        #print("no")
        next_bttn = False
    elif soup.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'}) != None:
        next_bttn = True
    elif soup.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'}) == None:
        next_bttn = False
    return next_bttn


def parse_hh(vac_list, vacations):
    for vacation in vac_list:
        # pprint(vacation)
        vac_data = {}
        vac_data['site'] = "HH"
        vac_data['title'] = vacation.find('a', {'data-qa': "vacancy-serp__vacancy-title"}).getText()
        vac_data['link'] = vacation.find('a', {'data-qa': "vacancy-serp__vacancy-title"}).attrs['href'].split("?")[0]
        salary = vacation.find('div', {'class': "vacancy-serp-item__sidebar"})
        if salary.getText() == "":
            sal_min, sal_max = 0, 0
            sal_cur = "-"
        else:
            salary = salary.getText().replace(" ", "").replace(" ", "|")

            if salary.startswith("от"):
                sal_min = salary.split("|")[1]
                sal_max = 0
                sal_cur = salary.split("|")[2]
            elif salary.startswith("до"):
                sal_min = 0
                sal_max = salary.split("|")[1]
                sal_cur = salary.split("|")[2]
            else:
                sal_min = salary.split("|")[0].split("-")[0]
                sal_max = salary.split("|")[0].split("-")[1]
                sal_cur = salary.split("|")[1]
        vac_data['_id'] = int(re.search(r"\d+", vac_data['link'])[0])
        vac_data['salary_min'] = int(sal_min)
        vac_data['salary_max'] = int(sal_max)
        vac_data['salary_cur'] = sal_cur

        vacations.append(vac_data)
    return vacations

def parse_sj(vac_list, vacations):
    for vac in vac_list:
        vac_data = {}
        vac_data['site'] = "SJ"
        vac_data['title'] = vac.find('a').getText()
        vac_data['link'] = "https://www.superjob.ru" + vac.find('a').attrs['href'].split("?")[0]
        salary = vac.find('span', {'class': "f-test-text-company-item-salary"}).getText().replace("\xa0", "")
        sal_min, sal_max = 0, 0
        sal_cur = "-"

        if salary.endswith("/месяц"):

            salary = salary[:-6]
        if salary == "По договорённости":
            sal_min, sal_max = 0, 0
            sal_cur = "-"
        else:

            if salary.startswith("от"):
                salary = salary[2:]
                sal_min = re.search(r"\d+", salary)[0]
                sal_max = 0
                sal_cur = re.sub(r"\d+", r"", salary)
            elif salary.startswith("до"):
                salary = salary[2:]
                sal_min = 0
                sal_max = re.search(r"\d+", salary)[0]
                sal_cur = re.sub(r"\d+", r"", salary)
            elif "—" in salary:

                sal_cur = re.sub(r"\d+", r"", salary)[1:]
                salary = salary.replace(sal_cur, "")
                sal_min = salary.split("—")[0]
                sal_max = salary.split("—")[1]

            else:
                sal_min = re.search(r"\d+", salary)[0]
                sal_max = re.search(r"\d+", salary)[0]
                sal_cur = re.sub(r"\d+", r"", salary)
        vac_data['_id'] = int(re.search(r"\d+\.html", vac_data['link'])[0][:-5])
        vac_data['salary_min'] = int(sal_min)
        vac_data['salary_max'] = int(sal_max)
        vac_data['salary_cur'] = sal_cur
        vacations.append(vac_data)

    return vacations

def find_vac():
    vacations = []
    vac_search = input("Введите должность для поиска: ")
    search_pages = int(input("Сколько страниц считать?"))

    link = "https://russia.superjob.ru/vacancy/search"

    page = 1

    while True:
        params = {'keywords': vac_search, 'page': page}
        soup = get_soup(link, params)
        if_next = check_sj_pages(soup)
        print(f"Обработка SuperJpb страницы № {page}")
        vac_block = soup.find('div', {'class': '_1Ttd8 _2CsQi'})
        vac_list = vac_block.find_all('div', {'class': 'f-test-vacancy-item'})
        vacations = parse_sj(vac_list, vacations)
        page += 1
        if page > search_pages:
            break
        if page > 20:
            break
        if not if_next:
            break




    params = {'text': vac_search}
    soup = get_soup('https://hh.ru' + '/search/vacancy', params)
    hh_max_page = check_hh_pages(soup)
    print(f"На HeadHunter найдено {hh_max_page} страниц результатов.")

    vac_block = soup.find('div', {'class': 'vacancy-serp'})
    # vac_list = vac_block.findChildren(recursive=False)
    vac_list = vac_block.find_all('div', {'class': 'vacancy-serp-item'})
    print(f"Страница 1")
    parse_hh(vac_list, vacations)


    if search_pages > 1:
        if search_pages <= hh_max_page:
            for hh_page in range(1, search_pages):
                print(f"Страница {hh_page+1}")
                params = {'text': vac_search, 'page': hh_page}
                soup = get_soup('https://hh.ru' + '/search/vacancy', params)
                vac_block = soup.find('div', {'class': 'vacancy-serp'})

                vac_list = vac_block.find_all('div', {'class': 'vacancy-serp-item'})

                parse_hh(vac_list, vacations)
        else:
            for hh_page in range (1, hh_max_page):
                print(f"Страница {hh_page+1}")
                params = {'text': vac_search, 'page': hh_page}
                soup = get_soup('https://hh.ru' + '/search/vacancy', params)
                vac_block = soup.find('div', {'class': 'vacancy-serp'})
                #vac_list = vac_block.findChildren(recursive=False)
                vac_list = vac_block.find_all('div', {'class': 'vacancy-serp-item'})
                #vacations = vacations + parse_hh(vac_list)
                parse_hh(vac_list, vacations)
                print("Количество страниц в поиске больше введенных")
    return vacations


