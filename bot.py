import config
import logging
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from sqliter import SQLighter
from datetime import datetime

# задаём уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter('database.db')


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("«Я - ваш изгнанный пророк»")


# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id, message.from_user.username)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer(
        "Вы успешно подписались на постики!")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы и так не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписаны от постиков.")


@dp.message_handler(commands=['posts'])
async def post(message: types.Message):
    await message.answer(db.get_random_post())
    print('------------------------------------------', message.from_user.username, datetime.now())


async def posts(wait_for=3600):
    while True:
        await asyncio.sleep(wait_for)
        subscriptions = db.get_subscriptions()
        for s in subscriptions:
            await bot.send_message(s[1], text=db.get_random_post())
            print('------------------------------------------', s[-1], datetime.now())


# запускаем лонг поллинг
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(posts())
    executor.start_polling(dp, skip_updates=True)
