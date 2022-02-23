import sqlite3

import random


class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subs` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subs` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def subscriber_True(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT status FROM `subs` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(*result[0])

    def add_subscriber(self, user_id, nick, status=True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `subs` (`user_id`, `status`, 'nick') VALUES(?,?,?)",
                                       (user_id, status, nick))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subs` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def get_random_post(self):

        self.cursor.execute("SELECT COUNT (*) FROM posts")
        l_p = self.cursor.fetchone()[0]
        r = random.randint(1, l_p - 1)
        r_posts = self.cursor.execute("SELECT posts FROM `posts` WHERE `post_id` = ?", (r,)).fetchall()

        self.connection.commit()
        res = ','.join([str(i) for i in r_posts[0]])
        print(res)
        return res

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
