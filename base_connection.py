import datetime
import multiprocessing
import os
import sqlite3


db_lock = multiprocessing.Lock()


def _create_database():
    """
    Создает базу данных и таблицу Cookie_Profile, наполняет ее 15 записями,
     если еще не существует. Если таблица существует, то возвращает связь
     с таблицей
    :return:
    """

    if not os.path.exists('Cookie_Profile'):
        with sqlite3.connect('Cookie_Profile') as conn:
            conn.execute(
                '''CREATE TABLE Cookie_Profile (
                id INTEGER PRIMARY KEY NOT NULL, 
                created_at DATETIME NOT NULL, 
                cookie_value TEXT, 
                last_used_at DATETIME, 
                total_launches INTEGER DEFAULT 0
                )'''
            )
            now = datetime.datetime.now()
            for i in range(15):
                conn.execute(
                    'INSERT INTO Cookie_Profile (created_at) VALUES (?)',
                    (now,)
                )
    else:
        conn = sqlite3.connect('Cookie_Profile')

    return conn


def get_row(id_row):
    """
    Возвращает запись по id из базы данных
    :param id_row:
    :return:
    """

    conn = _create_database()
    with conn:
        curs = conn.cursor()
        curs.execute('SELECT * FROM Cookie_Profile WHERE id=?', (id_row,))
        row = curs.fetchone()

        return {
            'id': row[0],
            'created': row[1],
            'cookie': row[2],
            'last_run': row[3],
            'run_count': row[4],
        }


def update_row(id_row, cookie_value):
    """
    Обновляем запись в базе данных, используется блокировка процессов,
    так как sqlite не годится под большое количество соединении
    :param id_row:
    :param cookie_value:
    :return:
    """

    with db_lock:
        conn = _create_database()
        with conn:
            curs = conn.cursor()
            now = datetime.datetime.now()
            curs.execute(
                'UPDATE Cookie_Profile '
                'SET cookie_value=?, '
                'last_used_at=?, '
                'total_launches=total_launches+1 '
                'WHERE id=?', (cookie_value, now, id_row)
            )
    return f'ID:{id_row}, внесены изменения'
