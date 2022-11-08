import logging

from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime, timedelta

import config as cfg
import markups as nav

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)

# время бана:
BAN_TIME = 1

# функция для банов пользователей:
def until_date():
    return datetime.now() + timedelta(minutes=BAN_TIME)

# для бана пользователя:
OnlyReadPermissions = types.ChatPermissions(can_send_messages=False,
                                            can_send_media_messages=False,
                                            can_send_polls=False,
                                            can_send_other_messages=False,
                                            can_add_web_page_previews=False,
                                            can_change_info=False,
                                            can_invite_users=False,
                                            can_pin_messages=False)

# функция для проверки подписки пользователя на канал:
def check_sub_channel(chat_member):
    return chat_member['status'] != "left"

# приветствие нового пользователя в чате:
@dp.message_handler(content_types=["new_chat_members"])
async def user_joined(message: types.Message):
    await message.answer("Добро пожаловать!\nВ нашем чате запрещено материться и присылать ссылки!\nЧтобы отправлять сообщения, подпишитесь на канал а так же пройдите проверку зайдя к боту и нажмите /start!", reply_markup=nav.botMenu)

@dp.message_handler()
async def mess_handler(message: types.Message):
    # проверяем, подписан ли пользователь на канал:
    if check_sub_channel(await bot.get_chat_member(chat_id=cfg.CHANNEL_ID, user_id=message.from_user.id)):
        # проверка на слова, которые прописаны в cfg.WORDS:
        text = message.text.lower()
        for word in cfg.WORDS:
            if word in text:
                # await message.delete()
                # время бана 1 минута:
                until_date = datetime.now() + timedelta(minutes=BAN_TIME)
                await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.from_user.id, permissions=OnlyReadPermissions, until_date=until_date)
                await bot.delete_message(message.chat.id, message.message_id)

        # проверка на содержание ссылок при помощи entities, если ссылка есть в cfg.LINKS, то не удаляем:
        for entity in message.entities:
            if entity.type in ['url', 'text_link']:
                with_links = True
                for word in cfg.LINKS:
                    if word not in text:
                        # await message.delete()
                        # время бана 1 минута:
                        until_date = datetime.now() + timedelta(minutes=BAN_TIME)
                        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.from_user.id, permissions=OnlyReadPermissions, until_date=until_date)
                        await bot.delete_message(message.chat.id, message.message_id)
    else:
        await message.answer("Чтобы отправлять сообщения, подпишитесь на канал!", reply_markup=nav.channelMenu)
        await message.delete()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)