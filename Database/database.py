import sqlite3


class Database:
    def __init__(self, data):
        self.connect = sqlite3.connect(data)
        self.cursor = self.connect.cursor()
        if self.connect:
            print('Data base connected OK')

    def check_user(self, user_id):
        """Проверка пользователя на наличие в БД"""
        return bool(self.cursor.execute('SELECT * FROM users WHERE tg_id = ?', (user_id,)).fetchone())

    def check_count(self, user_id):
        """Получем количество посещений и имя пользователя"""
        return self.cursor.execute('SELECT count,name FROM users WHERE tg_id = ?', (user_id,)).fetchone()

    def add_chek_in(self, user_id):
        """Чек_ин пользователяв БД"""
        self.cursor.execute('UPDATE users SET count = count +1 WHERE tg_id = ?', (user_id,))
        self.connect.commit()

    async def add_user(self, state):
        """Добавление нового пользователя в БД"""
        async with state.proxy() as data:
            self.cursor.execute('INSERT INTO users VALUES (?,?,?,?)',
                                (data['id'], data['name'], data['phone'], data['count']))
            self.connect.commit()

    async def add_menu(self, state):
        """Добавление в меню карточки"""
        async with state.proxy() as data:
            self.cursor.execute('INSERT INTO menu(category,photo) VALUES (?,?)', (data['category'], data['photo']))
            self.connect.commit()

    def show_menu(self, category):
        """Вывод карточек меня из БД"""
        return self.cursor.execute('SELECT photo, id FROM menu WHERE category = ?', (category,)).fetchall()

    async def del_from_menu(self, file_id):
        self.cursor.execute("""DELETE FROM menu WHERE id = ?""", (file_id,))
        self.connect.commit()

    def spam(self):
        """Получить id пользователей"""
        return self.cursor.execute('SELECT tg_id FROM users').fetchall()


db = Database('loft_data.db')
