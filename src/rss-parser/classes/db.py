import sqlite3

class Database:
    def __init__(self):
        self.db_url = "sqlite.db"
        self.cursor, self.connection = self.connect()
        self.prepare()

    def prepare(self): # создаём в бд таблицы если их не существует
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS News (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        link TEXT NOT NULL,
        category TEXT NOT NULL,
        author TEXT,
        full_text TEXT NOT NULL,
        pub_date TEXT NOT NULL
        );
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Chats (
        id INTEGER PRIMARY KEY,
        chat_id INTEGER NOT NULL UNIQUE
        );
        ''')
        # Сохраняем изменения
        self.connection.commit()
        
    def add_chat(self, chat_id):
        try: # игнорим ошибку потому что поле chat_id уникальное
            self.cursor.execute("INSERT INTO Chats(chat_id) VALUES (?);", (chat_id,))
            self.connection.commit()
        except:
            pass

    def get_all_chats(self): # получаем все чаты
        self.cursor.execute("SELECT chat_id FROM Chats;")
        chat_ids = self.cursor.fetchall()
        return chat_ids
    
    def connect(self): # подключение к бд
            connection = sqlite3.connect(self.db_url)
            cursor = connection.cursor()
            return cursor, connection
    
    def create_news(self, title, link, category, author, full_text, pub_date): # добавляем в бд новость
        self.cursor.execute("INSERT INTO News(title, link, category, author, full_text, pub_date) VALUES (?,?,?,?,?,?);",
                            (title, link, category, author,full_text, pub_date))
        self.connection.commit()