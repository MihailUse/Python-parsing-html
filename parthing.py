import requests
import csv

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

max_amount_pages = 100
columns = ['vacancy', 'link', 'responsibility', 'skills']  # название колонок в csv

# определиние диалекта и определение колонок
csv.register_dialect('my_dialect', quoting=csv.QUOTE_NONNUMERIC, delimiter=";", lineterminator="\r")
with open('parthing.csv', 'w', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns, dialect='my_dialect')
    writer.writeheader()

# первый запрос для получения данных о кол. страниц для дальнейшей работы с ними
url = 'https://spb.hh.ru/catalog/Informacionnye-tehnologii-Internet-Telekom'  # url страницы
r = requests.get(url, headers={'User-Agent': UserAgent().chrome}).text
soup = BeautifulSoup(r, 'html.parser')

page_count = int(soup.find_all('span', class_='pager-item-not-in-short-range')[2].find('a').get_text())
print('Количество cтраниц: ', page_count)

# перебор кождой страницы
for page in range(page_count):
    print(page)
    result = []  # массив с ваканиями с каждой страницы
    # ограничение обрабатываемых страниц
    if page == max_amount_pages:
        break

    # url для страницы
    url = 'https://spb.hh.ru/catalog/Informacionnye-tehnologii-Internet-Telekom?page={}'.format(page)
    r = requests.get(url, headers={'User-Agent': UserAgent().chrome}).text
    soup = BeautifulSoup(r, 'html.parser')

    posts = soup.find('div', class_='vacancy-serp').find_all('div', {'class': 'vacancy-serp-item'})
    print('Количество постов на странице %i: ' % (page + 1), len(posts))

    # перебор каждой вакансии на странице (posts)
    for post in posts:
        vacancy = post.find('a', class_='bloko-link HH-LinkModifier').text
        vacancy_link = post.find('a', class_='bloko-link HH-LinkModifier', href=True)['href']
        responsibility = post.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text or \
                         'Обязанности не найдены'

        # получение требуемых умений
        try:
            r = requests.get(vacancy_link, headers={'User-Agent': UserAgent().chrome}).text
            soup = BeautifulSoup(r, 'html.parser')

            all_skills = soup.find('div', class_='bloko-tag-list').find_all('span', {'data-qa': 'bloko-tag__text'})
            skills = []
            for el in all_skills:
                skills.append(el.text)
            skills = ', '.join(skills)
        except:
            skills = 'Не удалось получить доступ к вакансии или же теги не указаны'

        result.append([vacancy, vacancy_link, responsibility, skills])

    # добавление вакансий в файл
    with open('parthing.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f, 'my_dialect')
        writer.writerows(result)
