import requests
import time
import connect  # settings
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

max_amount_pages = 100
# max_amount_pages = int(input('Ограничение страниц: '))
start_time = time.time()

check = "SELECT id FROM it_vacancy WHERE vacancy = %s AND vacancy_link = %s AND text = %s AND skills = %s"
sql = "INSERT INTO `it_vacancy` (`vacancy`, `vacancy_link`, `text`, `skills`) VALUES (%s, %s, %s, %s)"

url = 'https://spb.hh.ru/catalog/Informacionnye-tehnologii-Internet-Telekom'  # url для страницы
r = requests.get(url, headers={'User-Agent': UserAgent().chrome}).text
soup = BeautifulSoup(r, 'html.parser')

# оооооооооооооооооочень криво
page_count = int(soup.find_all('span', class_='pager-item-not-in-short-range')[2].find('a').get_text())
print('Количество страниц: ', page_count)

# перебор кождой страницы
for page in range(page_count):
    result_page = []
    # ограничение обрабатываемых страниц
    if page == max_amount_pages:
        break

    url = 'https://spb.hh.ru/catalog/Informacionnye-tehnologii-Internet-Telekom?page={}'.format(page)  # url для страницы
    r = requests.get(url, headers={'User-Agent': UserAgent().chrome}).text
    soup = BeautifulSoup(r, 'html.parser')

    posts = soup.find('div', class_='vacancy-serp').find_all('div', {'class': 'vacancy-serp-item'})
    print('Количество постов на странице: ', len(posts))

    # перебор каждого поста и добавление в файл  len(posts)
    for post in range(len(posts)):
        vacancy = posts[post].find('a', class_='bloko-link HH-LinkModifier').text
        vacancy_link = posts[post].find('a', class_='bloko-link HH-LinkModifier', href=True)['href']
        responsibility = posts[post].find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text or \
                         'Обязанности не найдены'
        # print(post + 1, vacancy, vacancy_link)

        # получение тегов
        try:
            r = requests.get(vacancy_link, headers={'User-Agent': UserAgent().chrome}).text
            soup = BeautifulSoup(r, 'html.parser')

            all_skills = soup.find('div', class_='bloko-tag-list').find_all('span', {'data-qa': 'bloko-tag__text'})
            skills = []
            for row in all_skills:
                skills.append(row.text)
            skills = ', '.join(skills)
        except:
            skills = 'Не удалось получить доступ к вакансии или же теги не указаны'

        result_page.append([vacancy, vacancy_link, responsibility, skills])

    # подключение к бд
    connection = connect.getConnection()
    try:
        # специальный объект который делает запросы и получает их результаты
        cursor = connection.cursor()

        for row in result_page:
            review = cursor.execute(check, row)
            if review:
                continue
            else:
                cursor.execute(sql, row)

        # cursor.executemany(sql, result_page)
        connection.commit()
    finally:
        connection.close()

    print("--- page load time %s seconds ---" % (time.time() - start_time))

print("--- execution time %s seconds ---" % (time.time() - start_time))
