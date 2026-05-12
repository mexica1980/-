from order import Order, get_orders_by_client_id
from user import get_user_by_id
from datetime import datetime
import math

def calculate_distance(address1, address2):
    """Упрощенный расчет расстояния (для демонстрации)"""
    # В реальном приложении здесь был бы API карт
    # Для демо используем случайное расстояние от 1 до 30 км
    import random
    return round(random.uniform(1, 30), 1)

def show_order_details(order, user_role='client'):
    """Показывает детали заказа"""
    status_ru = {
        'waiting': ' Ожидает водителя',
        'accepted': ' Принят водителем',
        'in_progress': ' В пути',
        'completed': ' Завершен',
        'cancelled': ' Отменен'
    }
    
    print("\n" + "="*50)
    print(f" ЗАКАЗ #{order.id}")
    print("="*50)
    print(f"Откуда: {order.from_address}")
    print(f"Куда: {order.to_address}")
    print(f"Расстояние: {order.distance} км")
    print(f"Стоимость: {order.price} руб.")
    print(f"Статус: {status_ru.get(order.status, order.status)}")
    print(f"Создан: {order.created_date}")
    
    if order.completed_date:
        print(f" Завершен: {order.completed_date}")
    
    if order.driver_id:
        from user import get_user_by_id
        driver = get_user_by_id(order.driver_id)
        if driver:
            print(f"Водитель: {driver.name}")
    
    if order.client_rating and user_role == 'client':
        print(f"Ваша оценка водителю: {order.client_rating}/5")
    if order.driver_rating and user_role == 'driver':
        print(f"Оценка пассажира: {order.driver_rating}/5")
    
    print("="*50)

def create_order(client_id):
    """Создание нового заказа"""
    print("\n" + "="*50)
    print("           СОЗДАНИЕ НОВОГО ЗАКАЗА")
    print("="*50)
    
    from_address = input(" Откуда едем? (адрес): ")
    to_address = input(" Куда едем? (адрес): ")
    
    if not from_address or not to_address:
        print(" Адреса не могут быть пустыми")
        return None
    
    # Расчет расстояния и стоимости
    distance = calculate_distance(from_address, to_address)
    
    order = Order(
        client_id=client_id,
        from_address=from_address,
        to_address=to_address,
        distance=distance,
        status='waiting'
    )
    order.calculate_price()
    order.save()
    
    print(f"\n ЗАКАЗ СОЗДАН! ID: {order.id}")
    print(f"Расстояние: {distance} км")
    print(f"Стоимость: {order.price} руб.")
    print("\n Ожидаем подтверждения водителя...")
    
    return order

def show_my_orders(client_id):
    """Показать историю заказов клиента"""
    orders = get_orders_by_client_id(client_id)
    
    if not orders:
        print("\n У вас пока нет заказов")
        return
    
    status_ru = {
        'waiting': ' Ожидает',
        'accepted': ' Принят',
        'in_progress': ' В пути',
        'completed': ' Завершен',
        'cancelled': ' Отменен'
    }
    
    print("\n" + "="*50)
    print("           ИСТОРИЯ ЗАКАЗОВ")
    print("="*50)
    
    for o in orders:
        print(f"\n#{o.id} | {status_ru.get(o.status, o.status)} | {o.created_date[:16]}")
        print(f"   {o.from_address[:30]} → {o.to_address[:30]}")
        print(f"    {o.price} руб.")
    
    # Предложить посмотреть детали
    order_id = input("\nВведите ID заказа для деталей (0 - назад): ")
    if order_id.isdigit() and int(order_id) > 0:
        for o in orders:
            if o.id == int(order_id):
                show_order_details(o, 'client')
                # Если заказ завершен, можно оценить
                if o.status == 'completed' and not o.client_rating:
                    rate_driver(o)
                break

def rate_driver(order):
    """Оценить водителя после поездки"""
    print("\n ОЦЕНКА ПОЕЗДКИ")
    print("Оцените водителя от 1 до 5:")
    print("1 - Ужасно, 2 - Плохо, 3 - Нормально, 4 - Хорошо, 5 - Отлично")
    
    try:
        rating = int(input("Ваша оценка: "))
        if 1 <= rating <= 5:
            order.client_rating = rating
            order.save()
            print(f"Спасибо за оценку! Водитель получил {rating}/5")
            
            # Обновляем рейтинг водителя
            if order.driver_id:
                from driver import get_driver_by_user_id
                driver_info = get_driver_by_user_id(order.driver_id)
                if driver_info:
                    # Пересчитываем средний рейтинг
                    from order import get_orders_by_driver_id
                    driver_orders = get_orders_by_driver_id(order.driver_id)
                    ratings = [o.client_rating for o in driver_orders if o.client_rating]
                    if ratings:
                        new_rating = sum(ratings) / len(ratings)
                        driver_info.rating = round(new_rating, 1)
                        driver_info.save()
                        print(f"Новый рейтинг водителя: {driver_info.rating}/5")
        else:
            print("Оценка должна быть от 1 до 5")
    except ValueError:
        print(" Введите число")

def cancel_order(client_id):
    """Отмена активного заказа"""
    from order import get_active_orders
    
    active_orders = [o for o in get_active_orders() if o.client_id == client_id]
    
    if not active_orders:
        print("\n У вас нет активных заказов для отмены")
        return
    
    print("\nАКТИВНЫЕ ЗАКАЗЫ:")
    for o in active_orders:
        print(f"  #{o.id} | {o.from_address} → {o.to_address} | {o.status}")
    
    order_id = input("\nВведите ID заказа для отмены (0 - назад): ")
    if order_id.isdigit() and int(order_id) > 0:
        for o in active_orders:
            if o.id == int(order_id):
                if o.status in ['waiting', 'accepted']:
                    o.cancel()
                    print(f"Заказ #{o.id} отменен")
                else:
                    print(f"Нельзя отменить заказ в статусе '{o.status}'")
                break

def menu_client(user):
    """Главное меню клиента"""
    while True:
        print("\n" + "="*50)
        print(f"   ДОБРО ПОЖАЛОВАТЬ, {user.name.upper()}!")
        print("          МЕНЮ КЛИЕНТА")
        print("="*50)
        print("1.Создать заказ")
        print("2.Мои заказы")
        print("3.Отменить заказ")
        print("4.Мой профиль")
        print("0.Выйти из аккаунта")
        print("-"*50)
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            create_order(user.id)
        
        elif choice == "2":
            show_my_orders(user.id)
        
        elif choice == "3":
            cancel_order(user.id)
        
        elif choice == "4":
            print("\n" + "="*50)
            print("           ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ")
            print("="*50)
            print(f"Имя: {user.name}")
            print(f"Телефон: {user.phone}")
            print(f"Логин: {user.login}")
            print(f"Роль: {user.role}")
            print(f"Дата регистрации: {user.created_date[:16]}")
            input("\nНажмите Enter для продолжения...")
        
        elif choice == "0":
            print(f"\nДо свидания, {user.name}!")
            break
        else:
            print("\nНеверный ввод")