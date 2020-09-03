import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url = 'https://spb.hh.ru/search/vacancy?area=2&clusters=true&enable_snippets=true&specialization=1&only_with_salary=true&from=cluster_compensation&showClusters=true&page=0'  # url для страницы
r = requests.get(url, headers={'User-Agent': UserAgent().chrome}).text

soup = BeautifulSoup(r, 'html.parser')

all_vacancy = soup.find("div", class_="vacancy-serp").find_all("a", class_="bloko-link HH-LinkModifier")
all_link = soup.find("div", class_="vacancy-serp").find_all("a", class_="bloko-link HH-LinkModifier", href=True)
all_pay = soup.find("div", class_="vacancy-serp").find_all("span", {"data-qa": "vacancy-serp__vacancy-compensation"})

# i = 0
#  while i < 10:
#     all_hrefs

data = [['name_vacancy', 'vacancy_link', 'pay']]  # columns


i = len(all_vacancy)
print(i)
for el in range(len(all_vacancy)):
    vacancy = all_vacancy[el].get_text()  # name_vacancy
    link = all_link[el]['href']  # vacancy_link
    pay = all_pay[el].get_text()  # pay

    result = [vacancy, link, pay]
    data.append(result)

# print(row)

# 'a', encoding='utf-8'
with open('hhh.csv', 'w') as f:
    writer = csv.writer(f)
    for row in data:
        print(row)
        writer.writerow(row)
