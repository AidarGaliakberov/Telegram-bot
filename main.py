import logging
import sqlite3

from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime, timedelta

import config as cfg
import markups as nav
from db import Database

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot, dispatcher and database
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')

# Права при бане пользователя:
OnlyReadPermissions = types.ChatPermissions(can_send_messages=False,
                                            can_send_media_messages=False,
                                            can_send_polls=False,
                                            can_send_other_messages=False,
                                            can_add_web_page_previews=False,
                                            can_change_info=False,
                                            can_invite_users=False,
                                            can_pin_messages=False)

# Функция для проверки подписки пользователя на канал:
def check_sub_channel(chat_member):
    return chat_member['status'] != "left"

# Приветствие нового пользователя в чате:
@dp.message_handler(content_types=["new_chat_members"])
async def user_joined(message: types.Message):
    await message.answer(cfg.hello_msg_text, reply_markup=nav.botMenu)

@dp.message_handler()
async def mess_handler(message: types.Message):
    # Проверка пользователя записан ли он в БД:
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)

    # Проверяем, подписан ли пользователь на канал:
    if check_sub_channel(await bot.get_chat_member(chat_id=cfg.CHANNEL_ID, user_id=message.from_user.id)):

        # Проверка на слова, которые прописаны в cfg.WORDS:
        text = message.text.lower()
        for word in cfg.WORDS:
            if word in text:
                if str(message.from_user.id) != cfg.ADMIN_ID:
                    # Mention to user
                    user_id = message.from_user['id']
                    first_name = message.from_user['first_name']
                    mention = "[" + first_name + "](tg://user?id=" + str(user_id) + ")"

                    #Подключаемся к БД:
                    conn = sqlite3.connect('database.db')
                    user_mute_time = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
                    mute_time = user_mute_time[2]
                    if mute_time == 3:
                        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.from_user.id,
                                                       permissions=OnlyReadPermissions, until_date=cfg.until_date)

                    # Бот удаляет сообщение за нарушение правил:
                    await bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id, text=mention + ', Ваше сообщение удалено за нарушение правил! ' + str(mute_time) + ' из 3', parse_mode="Markdown")

                    # Пишем событие нарушения пользователя в БД:
                    db.add_user_violations(message.from_user.id)

                    # Удаляем сообщение:
                    await bot.delete_message(message.chat.id, message.message_id)

        # Проверка на содержание ссылок при помощи entities, если ссылка есть в cfg.LINKS, то не удаляем:
        for entity in message.entities:
            # Проверяем наличие ссылок в сообщении пользователя:
            if entity.type in ['url', 'text_link']:
                with_links = True
                for word in cfg.LINKS:
                    if word not in text:
                        if str(message.from_user.id) != cfg.ADMIN_ID:
                            user_id = message.from_user['id']
                            first_name = message.from_user['first_name']
                            mention = "[" + first_name + "](tg://user?id=" + str(user_id) + ")"

                            # Подключаемся к БД:
                            conn = sqlite3.connect('database.db')
                            user_mute_time = conn.execute("SELECT * FROM users WHERE user_id = ?",
                                                          (user_id,)).fetchone()
                            mute_time = user_mute_time[2]
                            if mute_time == 3:
                                await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.from_user.id,
                                                               permissions=OnlyReadPermissions, until_date=cfg.until_date)

                            # Бот удаляет сообщение за нарушение правил:
                            await bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id, text=mention + ', Ваше сообщение удалено за нарушение правил! ' + str(mute_time) + ' из 3', parse_mode="Markdown")

                            # Пишем событие нарушения пользователя в БД:
                            db.add_user_violations(message.from_user.id)

                            # Удаляем сообщение:
                            await bot.delete_message(message.chat.id, message.message_id)
    else:
        joined_user = str(message.from_user.first_name)
        await message.answer(joined_user + ", " + cfg.subscr_user_text, reply_markup=nav.channelMenu)
        await message.delete()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)