import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import time
start_time = time.time()

url = 'https://spb.hh.ru/search/vacancy?area=2&clusters=true&enable_snippets=true&specialization=1&only_with_salary=true&from=cluster_compensation&showClusters=true&page=0'  # url для страницы
r = requests.get(url, headers={'User-Agent': UserAgent().chrome}).text
soup = BeautifulSoup(r, 'html.parser')

all_vacancy = soup.find('div', class_='vacancy-serp').find_all('a', class_='bloko-link HH-LinkModifier')
all_link = soup.find('div', class_='vacancy-serp').find_all('a', class_='bloko-link HH-LinkModifier', href=True)
all_pay = soup.find('div', class_='vacancy-serp').find_all('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})

page_len = soup.find_all('span', class_='pager-item-not-in-short-range')[2].find('a').text  # оооооооооооооооооочень криво
print('Количество cтраниц: ', page_len)
for i in range(int(page_len) - 1):
    url = 'https://spb.hh.ru/search/vacancy?area=2&clusters=true&enable_snippets=true&specialization=1&only_with_salary=true&from=cluster_compensation&showClusters=true&page={i}'  # url для страницы
    r = requests.get(url, headers={'User-Agent': UserAgent().chrome}).text
    soup = BeautifulSoup(r, 'html.parser')

    # массивы должны быть большими, очень большими...
    all_vacancy += (soup.find('div', class_='vacancy-serp').find_all('a', class_='bloko-link HH-LinkModifier'))
    all_link += (soup.find('div', class_='vacancy-serp').find_all('a', class_='bloko-link HH-LinkModifier', href=True))
    all_pay += (soup.find('div', class_='vacancy-serp').find_all('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}))
    print('button exists on this page: ', i + 1)
    i += 1

    # ограничение страниц
    if i == 5:
        break


data = [['name_vacancy', 'vacancy_link', 'pay', 'skills']]  # columns

for el in range(len(all_vacancy)):
    vacancy = all_vacancy[el].get_text()
    link = all_link[el]['href']
    pay = all_pay[el].get_text()

    r = requests.get(link, headers={'User-Agent': UserAgent().chrome}).text
    soup = BeautifulSoup(r, 'html.parser')

    try:
        all_skills = soup.find('div', class_='bloko-tag-list')\
            .find_all('span', {'data-qa': 'bloko-tag__text'})
        skills = []
        for i in range(len(all_skills)):
            skills.append(all_skills[i].get_text())
        skills = ', '.join(skills)
    except:
        skills = 'Ключевые навыки не указаны'

    result = [vacancy, link, pay, skills]
    data.append(result)

# print(data)

# запись в csv файл
with open('hhh.csv', 'w') as f:
    writer = csv.writer(f, delimiter=';')
    for row in data:
        # print(row)
        writer.writerow(row)

print("--- execution time %s seconds ---" % (time.time() - start_time))