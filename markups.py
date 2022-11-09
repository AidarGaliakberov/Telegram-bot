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