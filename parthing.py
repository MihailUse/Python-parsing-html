import requests
import csv
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

start_time = time.time()

max_amount_pages = int(input('Ограничение страниц: '))

data = ['vacancy', 'vacancy_link', 'skills']  # columns

try:
    with open('parthing.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(data)
except:
    exit('Что-то пошло не так')

url = 'https://spb.hh.ru/catalog/Informacionnye-tehnologii-Internet-Telekom'  # url для страницы
r = requests.get(url, headers={'User-Agent': UserAgent().chrome}).text
soup = BeautifulSoup(r, 'html.parser')

page_count = int(soup.find_all('span', class_='pager-item-not-in-short-range')[2].find('a').get_text())  # оооооооооооооооооочень криво
print('Количество cтраниц: ', page_count)

# перебор кождой страницы
for page in range(page_count):
    # ограничение обрабатываемых страниц
    if page == max_amount_pages:
        break

    url = 'https://spb.hh.ru/catalog/Informacionnye-tehnologii-Internet-Telekom?page={page}'  # url для страницы
    r = requests.get(url, headers={'User-Agent': UserAgent().chrome}).text
    soup = BeautifulSoup(r, 'html.parser')

    posts = soup.find('div', class_='vacancy-serp').find_all('div', {'class': 'vacancy-serp-item'})
    print('Количество постов на странице: ', len(posts))

    # перебор каждого поста и добавление в файл
    for post in range(len(posts)):
        vacancy = posts[post].find('a', class_='bloko-link HH-LinkModifier').text
        vacancy_link = posts[post].find('a', class_='bloko-link HH-LinkModifier', href=True)['href']
        # print(post + 1, vacancy, vacancy_link)

        try:
            r = requests.get(vacancy_link, headers={'User-Agent': UserAgent().chrome}).text
            soup = BeautifulSoup(r, 'html.parser')

            all_skills = soup.find('div', class_='bloko-tag-list').find_all('span', {'data-qa': 'bloko-tag__text'})
            skills = []
            for el in range(len(all_skills)):
                skills.append(all_skills[el].text)
            skills = ', '.join(skills)
        except:
            skills = 'Не удалось получить доступ к вакансии или же теги не указаны'

        result = [vacancy, vacancy_link, skills]

        with open('parthing.csv', 'a') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(result)

    print("--- page load time %s seconds ---" % (time.time() - start_time))

print("--- execution time %s seconds ---" % (time.time() - start_time))
