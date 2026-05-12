import sqlite3
from config import DB_NAME

def get_connection():
    """Устанавливает соединение с базой данных"""
    return sqlite3.connect(DB_NAME)

def initialize_db():
    """Инициализирует базу данных: создает все таблицы"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Таблица пользователей (с логинами, паролями и ролями)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            phone TEXT,
            role TEXT CHECK(role IN ('client', 'driver', 'admin')) DEFAULT 'client',
            created_date TEXT
        )
    ''')
    
    # Таблица водителей (дополнительная информация)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            license_number TEXT,
            experience_years INTEGER DEFAULT 0,
            rating REAL DEFAULT 5.0,
            is_available INTEGER DEFAULT 1,
            current_location TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Таблица автомобилей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_id INTEGER UNIQUE,
            brand TEXT,
            model TEXT,
            license_plate TEXT UNIQUE,
            color TEXT,
            seats INTEGER DEFAULT 4,
            FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE
        )
    ''')
    
    # Таблица заказов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            driver_id INTEGER,
            from_address TEXT NOT NULL,
            to_address TEXT NOT NULL,
            distance REAL,
            price REAL,
            status TEXT CHECK(status IN ('waiting', 'accepted', 'in_progress', 'completed', 'cancelled')) DEFAULT 'waiting',
            created_date TEXT,
            completed_date TEXT,
            client_rating INTEGER,
            driver_rating INTEGER,
            FOREIGN KEY (client_id) REFERENCES users(id),
            FOREIGN KEY (driver_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(" База данных инициализирована")

def add_test_data():
    """Добавляет тестовые данные"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Проверяем, есть ли пользователи
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Администратор
        cursor.execute('''
            INSERT INTO users (login, password, name, phone, role, created_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('AndreiLog', 'Andrei1718', 'AndreiLoginov', '+7-991-346-91-24', 'admin', now))
        
        # Клиенты
        cursor.execute('''
            INSERT INTO users (login, password, name, phone, role, created_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('ivan', 'pass123', 'Иван Петров', '+7-924-101-14-17', 'client', now))
        
        cursor.execute('''
            INSERT INTO users (login, password, name, phone, role, created_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Artem', 'Artem181', ' Артем Бахров', '+7-967-231-86-34', 'client', now))
        
        # Водители
        cursor.execute('''
            INSERT INTO users (login, password, name, phone, role, created_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('driver1', 'rest', 'Никита Беляков', '+7-345-453-24-97', 'driver', now))
        
        cursor.execute('''
            INSERT INTO users (login, password, name, phone, role, created_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Andrei', 'Asdfg20210901', 'Андрей Воробей', '+7-910-905-24-90', 'driver', now))
        
        conn.commit()
        
        # Получаем ID водителей и добавляем информацию
        cursor.execute("SELECT id FROM users WHERE login = 'driver1'")
        driver1_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM users WHERE login = 'Andrei'")
        driver2_id = cursor.fetchone()[0]
        
        cursor.execute('''
            INSERT INTO drivers (user_id, license_number, experience_years, rating, is_available)
            VALUES (?, ?, ?, ?, ?)
        ''', (driver1_id, 'AA123456', 5, 4.9, 1))
        
        cursor.execute('''
            INSERT INTO drivers (user_id, license_number, experience_years, rating, is_available)
            VALUES (?, ?, ?, ?, ?)
        ''', (driver2_id, 'BB634588', 3, 5, 3))
        
        # Добавляем автомобили
        cursor.execute("SELECT id FROM drivers WHERE user_id = ?", (driver1_id,))
        driver1_db_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM drivers WHERE user_id = ?", (driver2_id,))
        driver2_db_id = cursor.fetchone()[0]
        
        cursor.execute('''
            INSERT INTO cars (driver_id, brand, model, license_plate, color, seats)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (driver1_db_id, 'Toyota', 'Camry', 'А123ВС', 'Белый', 4))
        
        cursor.execute('''
            INSERT INTO cars (driver_id, brand, model, license_plate, color, seats)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (driver2_db_id, 'Porshe', 'RSR3', 'В398DC', 'Светло-голубой', 2))
        
        conn.commit()
        print("Данные добавлены")
    
    conn.close()