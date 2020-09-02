import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url = 'https://spb.hh.ru/catalog/Informacionnye-tehnologii-Internet-Telekom'  # url для второй страницы
r = requests.get(url, headers={'User-Agent': UserAgent().chrome}).text

# def write_csv(data):\n",
#     with open('hh.csv', 'a', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow((data['name_vacancy'],
#                          data['vacancy_link'],
#                          data['pay'])

# def get_html_data(r):
# url = get_html(url)


soup = BeautifulSoup(r, 'html.parser')

result = soup.find('div', class_="vacancy-serp").find_all("a", class_="bloko-link HH-LinkModifier")
all_hrefs = soup.find('div', class_="vacancy-serp").find_all("a", class_="bloko-link HH-LinkModifier", href=True)

# i = 0
# while i < 10:

for el in all_hrefs:
    print(el['href'])

# for el in all_hrefs:
#     print(el.get_text())
