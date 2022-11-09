from datetime import datetime, timedelta

# Токен нашего бота:
TOKEN = "5769775888:AAFYGuAL9OsLLu4imbl85lhlRkUMnUdw0g4"

# Ссылки и ID нашего канала и чата:
CHANNEL_URL = "https://t.me/testing_my_bot123"
CHANNEL_ID = "@testing_my_bot123"
CHAT_ID = "@aid_test_chat"
BOT_URL = "https://t.me/aid946_bot"

# ID админа:
ADMIN_ID = "422256031"

# Админка запрещенных слов:
WORDS = ['один', 'два', 'три']

# Админка разрешенных ссылок. Остальные ссылки все будут удаляться ботом автоматически:
LINKS = ['ya.ru']

# Текст приветствия:
hello_msg_text = "Добро пожаловать!\nВ нашем чате запрещено материться и присылать ссылки!\nЧтобы отправлять сообщения, подпишитесь на канал а так же пройдите проверку зайдя к боту и нажмите start!"

# Текст проверки подписки на канал:
subscr_user_text = "чтобы отправлять сообщения, подпишитесь на канал ниже!"

# Время блокировки (в данном случае в минутах (1 минута). Меняется в зависимости от параметра timedelta):
BAN_TIME = 1
until_date = datetime.now() + timedelta(minutes=BAN_TIME)
    # days - день,
    # seconds - секунды,
    # microseconds - микросекунды,
    # milliseconds - миллисекунды,
    # minutes - минуты,
    # hours - часы,
    # weeks - недели.