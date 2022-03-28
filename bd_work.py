import vk  # Импортируем модуль vk
import sqlite3
import random

from config import token

session = vk.Session(access_token=token)
vk_api = vk.API(session)
all_posts = []
connection = sqlite3.connect('database.db')
cursor = connection.cursor()


def get_post(us_id, kol, num_of, of=1):
    for it in range(num_of, kol):
        first = vk_api.wall.get(owner_id=us_id, count=kol, offset=of + num_of, v=5.92)  # Первое выполнение метода
        data = first["items"]
    for i in range(len(data)):
        all_posts.append(data[i]['text'])
    return all_posts, len(all_posts)


def save_data():  # Функция сохранения
    cursor.execute("SELECT COUNT (*) FROM posts")
    count = cursor.fetchone()[0] + 1
    print('Кол-во записей', count)
    for i in all_posts:
        cursor.execute("INSERT INTO `posts` (`post_id`, `posts`) VALUES(?,?)", (count, i))
        count += 1
        connection.commit()


def del_data():
    c = 0
    a = cursor.execute("SELECT * FROM posts ").fetchall()
    for i in a:
        # print(i[0])
        if len(i[1]) == 0:
            cursor.execute("DELETE FROM posts WHERE `post_id` = ?", (i[0],))
            connection.commit()
    # print(c)


def update_id():
    cursor.execute("SELECT COUNT (*) FROM posts")
    post_id = cursor.execute("SELECT post_id FROM posts").fetchall()
    old_id = []
    for i in post_id:
        old_id.append(i[0])
    for i in range(1, len(old_id) + 1):
        print(i, old_id[i - 1])
        cursor.execute("UPDATE posts SET post_id = ? WHERE post_id = ? ", (i, old_id[i - 1]))
        connection.commit()


def dubble():
    post_and_id = cursor.execute("SELECT *  FROM posts").fetchall()
    posts = []
    for i in post_and_id:
        posts.append(i[1])
        if posts.count(i[1]) > 1:
            cursor.execute("DELETE FROM posts WHERE `post_id` = ?", (i[0],))
            connection.commit()


def get_random_post():
    l_p = len(all_posts)
    r = random.randint(1, l_p)
    r_posts = cursor.execute("SELECT posts FROM `posts` WHERE `post_id` = ?", (r,)).fetchall()
    connection.commit()
    res = ','.join([str(i) for i in r_posts[0]])
    print(res)


while True:
    print("1. Получить посты. \n"
          "2. Сохранить в БД новых записей. \n"
          "3. Удалить пустые записи. \n"
          "4. Удалить дубликаты \n"
          "5. Обновить id. \n"

          "0. DONE. ")
    num_choise = input("Введите номер операции: ")
    if num_choise == '1':
        us_id = int(input('Введите id страницы или группы(-) '))
        num_of = int(input('Введите с какой записи '))
        kol = int(input('Введите по какую '))
        print(get_post(us_id, kol, num_of))
    elif num_choise == '2':
        save_data()
    elif num_choise == '3':
        del_data()
    elif num_choise == '4':
        dubble()
    elif num_choise == '5':
        update_id()
    elif num_choise == '0':
        break
