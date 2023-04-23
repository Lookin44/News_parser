import json
import multiprocessing
import logging

import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from base_connection import get_row, update_row
from utility import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_formatter = logging.Formatter('%(levelname)s - %(message)s')

console_handler.setFormatter(console_formatter)

logger.addHandler(console_handler)


def get_new_links():
    """
    Берем с https://news.google.com/home все ссылки на новости и возвращаем
    список из ссылок
    :return:
    """

    url = 'https://news.google.com/home'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_links = [
        f"{url}{link['href']}" for link in
        soup.find_all('a', href=True) if '/articles/' in link['href']
    ]
    response.close()
    logger.info(f'Собраны ссылки с сайта {url}')
    return news_links


def open_link(url, row: dict):
    """
    Открываем ссылку, выполняем рандомную задержку с имитацией прокрутки,
    достаем все куки и отправляем в таблицу
    :param url:
    :param row:
    :return:
    """

    name_proc = multiprocessing.current_process().name
    logger.info(f'Работает профиль {row["id"]} '
                f'Имя процесса: {name_proc}')

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    with Chrome(options=chrome_options) as browser:

        browser.get(url=url)

        if row['cookie']:
            cookies = json.loads(row['cookie'])
            browser.add_cookie(cookies[0])

        scroll_count = random.randint(1, 5)

        for i in range(scroll_count):
            scroll_page(browser)

        selenium_cookies = browser.get_cookies()

        update_row(row['id'], json.dumps(selenium_cookies))
        logger.info(f'Сохраняем куки для профиля: {row["id"]}')
        logger.info(f'Процесс {name_proc} завершен')


def main():
    """
    Голова скрипта, собирает профили и ссылки в список из множеств, передает
    на обработку в Selenium, для имитации просмотра ссылки с существующими
    cookies
    :return:

    """

    profile_work = [get_row(i) for i in range(1, 16)]
    links_list = get_new_links()
    random.shuffle(profile_work)
    random.shuffle(links_list)
    args = list(zip(links_list, profile_work))

    logger.info(f'Количество профилей: {len(args)}')

    with multiprocessing.Pool(processes=5) as pool:
        pool.starmap(open_link, args)


if __name__ == '__main__':

    # Бесконечный цикл который будет собирать,
    # открывать ссылки и обновлять cookie каждые 45 секунд
    while True:
        logger.info(f'------------------------')
        logger.info(f'----Начало цикла--------')
        logger.info(f'------------------------')
        main()
        logger.info(f'------------------------')
        logger.info(f'-----Конец цикла--------')
        logger.info(f'------------------------')
        time.sleep(45)
