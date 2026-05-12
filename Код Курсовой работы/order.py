from database import get_connection
from datetime import datetime
import random

class Order:
    def __init__(self, id=None, client_id=None, driver_id=None, 
                 from_address=None, to_address=None, distance=None, 
                 price=None, status='waiting', created_date=None, 
                 completed_date=None, client_rating=None, driver_rating=None):
        self.id = id
        self.client_id = client_id
        self.driver_id = driver_id
        self.from_address = from_address
        self.to_address = to_address
        self.distance = distance
        self.price = price
        self.status = status
        self.created_date = created_date if created_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.completed_date = completed_date
        self.client_rating = client_rating
        self.driver_rating = driver_rating
    
    def save(self):
        """Сохраняет заказ"""
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute('''
                INSERT INTO orders (client_id, driver_id, from_address, to_address, 
                                   distance, price, status, created_date, completed_date,
                                   client_rating, driver_rating)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.client_id, self.driver_id, self.from_address, self.to_address,
                  self.distance, self.price, self.status, self.created_date,
                  self.completed_date, self.client_rating, self.driver_rating))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE orders 
                SET client_id = ?, driver_id = ?, from_address = ?, to_address = ?,
                    distance = ?, price = ?, status = ?, completed_date = ?,
                    client_rating = ?, driver_rating = ?
                WHERE id = ?
            ''', (self.client_id, self.driver_id, self.from_address, self.to_address,
                  self.distance, self.price, self.status, self.completed_date,
                  self.client_rating, self.driver_rating, self.id))
        
        conn.commit()
        conn.close()
    
    def calculate_price(self):
        """Расчет стоимости поездки (100 руб/км + коэффициент)"""
        if self.distance:
            base_price = self.distance * 100
            # Случайный коэффициент спроса 1.0 - 2.0
            multiplier = random.uniform(1.0, 2.0)
            self.price = round(base_price * multiplier, 2)
        return self.price
    
    def accept_by_driver(self, driver_id):
        """Водитель принимает заказ"""
        self.driver_id = driver_id
        self.status = 'accepted'
        self.save()
        
        # Обновляем статус водителя на занят
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE drivers SET is_available = 0 WHERE user_id = ?", (driver_id,))
        conn.commit()
        conn.close()
    
    def start_trip(self):
        """Начать поездку"""
        self.status = 'in_progress'
        self.save()
    
    def complete_trip(self, client_rating=None, driver_rating=None):
        """Завершить поездку с оценками"""
        self.status = 'completed'
        self.completed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.client_rating = client_rating
        self.driver_rating = driver_rating
        self.save()
        
        # Обновляем статус водителя на свободен
        if self.driver_id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE drivers SET is_available = 1 WHERE user_id = ?", (self.driver_id,))
            conn.commit()
            conn.close()
    
    def cancel(self):
        """Отменить заказ"""
        self.status = 'cancelled'
        self.save()
        
        # Если водитель был назначен, освобождаем его
        if self.driver_id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE drivers SET is_available = 1 WHERE user_id = ?", (self.driver_id,))
            conn.commit()
            conn.close()

def get_all_orders():
    """Возвращает все заказы"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, client_id, driver_id, from_address, to_address, 
               distance, price, status, created_date, completed_date, 
               client_rating, driver_rating
        FROM orders
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [Order(id=row[0], client_id=row[1], driver_id=row[2], 
                  from_address=row[3], to_address=row[4], distance=row[5],
                  price=row[6], status=row[7], created_date=row[8],
                  completed_date=row[9], client_rating=row[10], driver_rating=row[11]) 
            for row in rows]

def get_order_by_id(order_id):
    """Возвращает заказ по ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, client_id, driver_id, from_address, to_address, 
               distance, price, status, created_date, completed_date,
               client_rating, driver_rating
        FROM orders WHERE id = ?
    ''', (order_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Order(id=row[0], client_id=row[1], driver_id=row[2], 
                     from_address=row[3], to_address=row[4], distance=row[5],
                     price=row[6], status=row[7], created_date=row[8],
                     completed_date=row[9], client_rating=row[10], driver_rating=row[11])
    return None

def get_orders_by_client_id(client_id):
    """Возвращает заказы клиента"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, client_id, driver_id, from_address, to_address, 
               distance, price, status, created_date, completed_date,
               client_rating, driver_rating
        FROM orders WHERE client_id = ? ORDER BY created_date DESC
    ''', (client_id,))
    rows = cursor.fetchall()
    conn.close()
    return [Order(id=row[0], client_id=row[1], driver_id=row[2], 
                  from_address=row[3], to_address=row[4], distance=row[5],
                  price=row[6], status=row[7], created_date=row[8],
                  completed_date=row[9], client_rating=row[10], driver_rating=row[11]) 
            for row in rows]

def get_orders_by_driver_id(driver_id):
    """Возвращает заказы водителя"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, client_id, driver_id, from_address, to_address, 
               distance, price, status, created_date, completed_date,
               client_rating, driver_rating
        FROM orders WHERE driver_id = ? ORDER BY created_date DESC
    ''', (driver_id,))
    rows = cursor.fetchall()
    conn.close()
    return [Order(id=row[0], client_id=row[1], driver_id=row[2], 
                  from_address=row[3], to_address=row[4], distance=row[5],
                  price=row[6], status=row[7], created_date=row[8],
                  completed_date=row[9], client_rating=row[10], driver_rating=row[11]) 
            for row in rows]

def get_active_orders():
    """Возвращает активные заказы (waiting, accepted, in_progress)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, client_id, driver_id, from_address, to_address, 
               distance, price, status, created_date, completed_date,
               client_rating, driver_rating
        FROM orders WHERE status IN ('waiting', 'accepted', 'in_progress')
        ORDER BY created_date
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [Order(id=row[0], client_id=row[1], driver_id=row[2], 
                  from_address=row[3], to_address=row[4], distance=row[5],
                  price=row[6], status=row[7], created_date=row[8],
                  completed_date=row[9], client_rating=row[10], driver_rating=row[11]) 
            for row in rows]