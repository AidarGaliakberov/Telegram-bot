import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    # Проверяем, есть ли пользователь в БД:
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'users' WHERE 'user_id' = ?", (user_id,)).fetchall()
            return bool(len(result))

    # Добавляем пользователя в БД если его нет:
    def add_user(self, user_id):
        with self.connection:
            try:
                return self.connection.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))
            except:
                pass

    # Добавляем в БД факт нарушения правил пользователем:
    def add_user_violations(self, user_id):
        with self.connection:
            user = self.connection.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
            # Считываем из БД количество нарушений пользователя:
            mute_time = user[2]

            #Условие для бана пользователя 3 нарушения:
            if mute_time < 3:
                return self.connection.execute("""UPDATE users SET mute_time = ? WHERE user_id = ?""", (mute_time + 1, user_id,))
            else:
                return self.connection.execute("""UPDATE users SET mute_time = ? WHERE user_id = ?""", (1, user_id,))
