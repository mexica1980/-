from database import get_connection
from datetime import datetime

class User:
    def __init__(self, id=None, login=None, password=None, name=None, 
                 phone=None, role='client', created_date=None):
        self.id = id
        self.login = login
        self.password = password
        self.name = name
        self.phone = phone
        self.role = role
        self.created_date = created_date if created_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def save(self):
        """Сохраняет пользователя (регистрация или обновление)"""
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute('''
                INSERT INTO users (login, password, name, phone, role, created_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.login, self.password, self.name, self.phone, self.role, self.created_date))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE users 
                SET login = ?, password = ?, name = ?, phone = ?, role = ?
                WHERE id = ?
            ''', (self.login, self.password, self.name, self.phone, self.role, self.id))
        
        conn.commit()
        conn.close()
    
    def delete(self):
        """Удаляет пользователя"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (self.id,))
            conn.commit()
            conn.close()

def authenticate(login, password):
    """Проверяет логин и пароль, возвращает пользователя или None"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, login, password, name, phone, role, created_date 
        FROM users WHERE login = ? AND password = ?
    ''', (login, password))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return User(id=row[0], login=row[1], password=row[2], name=row[3], 
                    phone=row[4], role=row[5], created_date=row[6])
    return None

def get_user_by_id(user_id):
    """Возвращает пользователя по ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, login, password, name, phone, role, created_date 
        FROM users WHERE id = ?
    ''', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return User(id=row[0], login=row[1], password=row[2], name=row[3],
                    phone=row[4], role=row[5], created_date=row[6])
    return None

def get_user_by_login(login):
    """Проверяет, существует ли логин"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE login = ?", (login,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def get_all_users():
    """Возвращает всех пользователей"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, login, password, name, phone, role, created_date FROM users")
    rows = cursor.fetchall()
    conn.close()
    return [User(id=row[0], login=row[1], password=row[2], name=row[3],
                 phone=row[4], role=row[5], created_date=row[6]) for row in rows]

def get_users_by_role(role):
    """Возвращает пользователей по роли"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, login, password, name, phone, role, created_date 
        FROM users WHERE role = ?
    ''', (role,))
    rows = cursor.fetchall()
    conn.close()
    return [User(id=row[0], login=row[1], password=row[2], name=row[3],
                 phone=row[4], role=row[5], created_date=row[6]) for row in rows]