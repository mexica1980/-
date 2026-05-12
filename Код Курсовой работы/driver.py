from database import get_connection

class Driver:
    def __init__(self, id=None, user_id=None, license_number=None, 
                 experience_years=0, rating=5.0, is_available=True, current_location=None):
        self.id = id
        self.user_id = user_id
        self.license_number = license_number
        self.experience_years = experience_years
        self.rating = rating
        self.is_available = is_available  # 1 - свободен, 0 - занят
        self.current_location = current_location
    
    def save(self):
        """Сохраняет информацию о водителе"""
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute('''
                INSERT INTO drivers (user_id, license_number, experience_years, rating, is_available, current_location)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.user_id, self.license_number, self.experience_years, 
                  self.rating, 1 if self.is_available else 0, self.current_location))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE drivers 
                SET license_number = ?, experience_years = ?, rating = ?, 
                    is_available = ?, current_location = ?
                WHERE id = ?
            ''', (self.license_number, self.experience_years, self.rating,
                  1 if self.is_available else 0, self.current_location, self.id))
        
        conn.commit()
        conn.close()
    
    def set_available(self, available):
        """Устанавливает статус доступности водителя"""
        self.is_available = available
        self.save()

def get_driver_by_user_id(user_id):
    """Возвращает водителя по ID пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, user_id, license_number, experience_years, rating, is_available, current_location
        FROM drivers WHERE user_id = ?
    ''', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Driver(id=row[0], user_id=row[1], license_number=row[2], 
                      experience_years=row[3], rating=row[4], 
                      is_available=row[5] == 1, current_location=row[6])
    return None

def get_all_drivers():
    """Возвращает всех водителей"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, user_id, license_number, experience_years, rating, is_available, current_location
        FROM drivers
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [Driver(id=row[0], user_id=row[1], license_number=row[2], 
                   experience_years=row[3], rating=row[4], 
                   is_available=row[5] == 1, current_location=row[6]) for row in rows]

def get_available_drivers():
    """Возвращает свободных водителей"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, user_id, license_number, experience_years, rating, is_available, current_location
        FROM drivers WHERE is_available = 1
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [Driver(id=row[0], user_id=row[1], license_number=row[2], 
                   experience_years=row[3], rating=row[4], 
                   is_available=True, current_location=row[6]) for row in rows]