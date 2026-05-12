from database import get_connection

class Car:
    def __init__(self, id=None, driver_id=None, brand=None, model=None,
                 license_plate=None, color=None, seats=4):
        self.id = id
        self.driver_id = driver_id
        self.brand = brand
        self.model = model
        self.license_plate = license_plate
        self.color = color
        self.seats = seats
    
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute('''
                INSERT INTO cars (driver_id, brand, model, license_plate, color, seats)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.driver_id, self.brand, self.model, self.license_plate, self.color, self.seats))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE cars SET brand = ?, model = ?, license_plate = ?, color = ?, seats = ?
                WHERE driver_id = ?
            ''', (self.brand, self.model, self.license_plate, self.color, self.seats, self.driver_id))
        
        conn.commit()
        conn.close()

def get_car_by_driver_id(driver_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, driver_id, brand, model, license_plate, color, seats
        FROM cars WHERE driver_id = ?
    ''', (driver_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Car(id=row[0], driver_id=row[1], brand=row[2], model=row[3],
                   license_plate=row[4], color=row[5], seats=row[6])
    return None