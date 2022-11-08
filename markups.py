from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config as cfg

btnUrlChannel = InlineKeyboardButton(text="Канал", url=cfg.CHANNEL_URL)
channelMenu = InlineKeyboardMarkup(row_width=1)
channelMenu.insert(btnUrlChannel)

botUrl = InlineKeyboardButton(text="Перейти к боту", url=cfg.BOT_URL)
botMenu = InlineKeyboardMarkup(row_width=1)
botMenu.insert(botUrl)