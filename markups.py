from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config as cfg
from aiogram import types

# Конфиги кнопок:

# Кнопка для перехода в канал:
btnUrlChannel = InlineKeyboardButton(text="Подписаться на канал", url=cfg.CHANNEL_URL)
channelMenu = InlineKeyboardMarkup(row_width=1)
channelMenu.insert(btnUrlChannel)

# Кнопка для перехода к боту:
botUrl = InlineKeyboardButton(text="Перейти к боту", url=cfg.BOT_URL)
botMenu = InlineKeyboardMarkup(row_width=1)
botMenu.insert(botUrl)

# Кнопка бота с приветствием и переходом в чат:
bot_btn = InlineKeyboardButton(text="👋 Перейти к чату", url=cfg.CHAT_URL)
hello_btn = InlineKeyboardMarkup(row_width=1)
hello_btn.insert(bot_btn)