# Задача

Создать проект на базе SQLite, Requests, Selenium, Multiprocessing. 
Получаем свежие новости из Google, создаем потоки на каждый профиль, 
создаем сессию используя уже имеющиеся Cookie, переходим и листаем новости, 
после чего добавляем новые Cookie в базу данных.

#### [Текст теста](https://docs.google.com/document/d/1n11Jvf4RJCwbA5eJkoOnFgZfeN3TwUSRG2suuDU1rn0/edit)

## Стек

* Python
* Requests
* Selenium
* BeautifulSoup 4

## Описание проекта

Скрипт работает до момента пока его не остановят принудительно. Одновременно
могут выполнять работу до 5 процессов, за это отвечает стандартная библиотека
[multiprocessing](https://docs.python.org/3/library/multiprocessing.html). 
За выполнение открытия и имитации просмотра ссылки отвечает модуль 
[Selenium](https://pypi.org/project/selenium/).
Модуль [requests](https://requests.readthedocs.io/en/latest/) 
парсит страницу с поддержкой 
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) со страницы
[Google новостей](https://news.google.com/home) 
и собирает их в словарь.

[sqlite](https://docs.python.org/3/library/sqlite3.html) выполняет соединение, 
вставку и обновление записей в базу данных. (Мнение автора проекта: 
писать прямые SQL-запросы не лучший вариант с точки зрения безопасности, 
я бы использовал ORM SQLAlchemy как минимум, в идеале ORM от Django)


## Запуск проекта
Скопируйте себе репозиторий
```git
git clone https://github.com/Lookin44/News_parser.git
```

Запустите docker-compose
```docker
docker-compose up -d
```