from order import Order, get_active_orders, get_orders_by_driver_id, get_order_by_id
from driver import get_driver_by_user_id
from user import get_user_by_id

def show_available_orders(driver_id):
    """Показать доступные заказы (ожидающие водителя)"""
    active_orders = get_active_orders()
    available_orders = [o for o in active_orders if o.status == 'waiting']
    
    if not available_orders:
        print("\n Нет доступных заказов")
        return None
    
    print("\n" + "="*50)
    print("           ДОСТУПНЫЕ ЗАКАЗЫ")
    print("="*50)
    
    for o in available_orders:
        client = get_user_by_id(o.client_id)
        client_name = client.name if client else "Неизвестно"
        print(f"\n ЗАКАЗ #{o.id}")
        print(f"{o.from_address} → {o.to_address}")
        print(f"{o.distance} км |  {o.price} руб.")
        print(f"Клиент: {client_name}")
    
    order_id = input("\nВведите ID заказа для принятия (0 - назад): ")
    if order_id.isdigit() and int(order_id) > 0:
        for o in available_orders:
            if o.id == int(order_id):
                return o
    return None

def accept_order(order, driver_id):
    """Принять заказ"""
    print(f"\n ПРИНЯТИЕ ЗАКАЗА #{order.id}")
    print(f"Откуда: {order.from_address}")
    print(f"Куда: {order.to_address}")
    print(f"Стоимость: {order.price} руб.")
    
    confirm = input("\nПодтвердить принятие? (да/нет): ")
    if confirm.lower() in ['да', 'yes', 'д', 'y']:
        order.accept_by_driver(driver_id)
        print(f" Заказ #{order.id} принят!")
        print("   Теперь вы можете начать поездку в меню 'Мои активные заказы'")
        return True
    return False

def show_my_active_orders(driver_id):
    """Показать активные заказы водителя"""
    all_driver_orders = get_orders_by_driver_id(driver_id)
    active_orders = [o for o in all_driver_orders if o.status in ['accepted', 'in_progress']]
    
    if not active_orders:
        print("\n Нет активных заказов")
        return None
    
    print("\n" + "="*50)
    print("        АКТИВНЫЕ ЗАКАЗЫ")
    print("="*50)
    
    status_ru = {
        'accepted': ' Принят (ожидает начала)',
        'in_progress': ' В пути'
    }
    
    for o in active_orders:
        client = get_user_by_id(o.client_id)
        print(f"\nЗАКАЗ #{o.id}")
        print(f"{o.from_address} → {o.to_address}")
        print(f"{o.price} руб.")
        print(f"Статус: {status_ru.get(o.status, o.status)}")
        print(f"Клиент: {client.name if client else 'Неизвестно'}")
    
    order_id = input("\nВведите ID заказа для управления (0 - назад): ")
    if order_id.isdigit() and int(order_id) > 0:
        for o in active_orders:
            if o.id == int(order_id):
                return o
    return None

def manage_active_order(order, driver_id):
    """Управление активным заказом"""
    while True:
        print("\n" + "="*50)
        print(f"        УПРАВЛЕНИЕ ЗАКАЗОМ #{order.id}")
        print("="*50)
        
        client = get_user_by_id(order.client_id)
        print(f"Клиент: {client.name if client else 'Неизвестно'}")
        print(f"Маршрут: {order.from_address} → {order.to_address}")
        print(f"Стоимость: {order.price} руб.")
        print(f"Текущий статус: {order.status}")
        
        print("\n ДОСТУПНЫЕ ДЕЙСТВИЯ:")
        
        if order.status == 'accepted':
            print("1.Начать поездку")
        elif order.status == 'in_progress':
            print("1.Завершить поездку")
        
        print("2.Информация о клиенте")
        print("0.Назад")
        print("-"*30)
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            if order.status == 'accepted':
                print("\nНАЧАЛО ПОЕЗДКИ")
                confirm = input("Подтвердите начало поездки (да/нет): ")
                if confirm.lower() in ['да', 'yes', 'д', 'y']:
                    order.start_trip()
                    print("Поездка начата! Счастливого пути!")
                    return True
            
            elif order.status == 'in_progress':
                print("\nЗАВЕРШЕНИЕ ПОЕЗДКИ")
                confirm = input("Подтвердите завершение поездки (да/нет): ")
                if confirm.lower() in ['да', 'yes', 'д', 'y']:
                    order.complete_trip()
                    print("Поездка завершена!")
                    print("Клиент сможет оценить вас позже")
                    return True
        
        elif choice == "2":
            if client:
                print("\n" + "="*50)
                print("        ИНФОРМАЦИЯ О КЛИЕНТЕ")
                print("="*50)
                print(f"Имя: {client.name}")
                print(f"Телефон: {client.phone}")
                input("\nНажмите Enter для продолжения...")
            else:
                print("Информация о клиенте не найдена")
        
        elif choice == "0":
            break
        else:
            print("Неверный ввод")
    
    return False

def show_completed_orders(driver_id):
    """Показать завершенные заказы водителя"""
    orders = get_orders_by_driver_id(driver_id)
    completed = [o for o in orders if o.status == 'completed']
    
    if not completed:
        print("\nНет завершенных заказов")
        return
    
    print("\n" + "="*50)
    print("        ЗАВЕРШЕННЫЕ ЗАКАЗЫ")
    print("="*50)
    
    total_earned = sum(o.price for o in completed)
    
    for o in completed:
        client = get_user_by_id(o.client_id)
        print(f"\n#{o.id} | {o.completed_date[:16]}")
        print(f"{o.from_address[:25]} → {o.to_address[:25]}")
        print(f"{o.price} руб.")
        if o.client_rating:
            print(f"    Оценка клиента: {o.client_rating}/5")
    
    print("\n" + "="*50)
    print(f"ВСЕГО ЗАРАБОТАНО: {total_earned} руб.")
    print(f"ВСЕГО ПОЕЗДОК: {len(completed)}")
    print("="*50)
    
    input("\nНажмите Enter для продолжения...")

def show_driver_profile(driver_id):
    """Показать профиль водителя"""
    from driver import get_driver_by_user_id
    from user import get_user_by_id
    
    driver_info = get_driver_by_user_id(driver_id)
    user = get_user_by_id(driver_id)
    
    if not driver_info or not user:
        print("Профиль не найден")
        return
    
    print("\n" + "="*50)
    print("           ПРОФИЛЬ ВОДИТЕЛЯ")
    print("="*50)
    print(f"Имя: {user.name}")
    print(f"Телефон: {user.phone}")
    print(f"Логин: {user.login}")
    print(f"Номер прав: {driver_info.license_number or 'Не указан'}")
    print(f"Опыт: {driver_info.experience_years} лет")
    print(f"Рейтинг: {driver_info.rating}/5")
    print(f"Статус: {'Свободен' if driver_info.is_available else 'Занят'}")
    
    # Статистика
    orders = get_orders_by_driver_id(driver_id)
    completed = [o for o in orders if o.status == 'completed']
    total_earned = sum(o.price for o in completed)
    
    print(f"\n СТАТИСТИКА:")
    print(f"Всего поездок: {len(completed)}")
    print(f"Заработано: {total_earned} руб.")
    
    input("\nНажмите Enter для продолжения...")

def menu_driver(user):
    """Главное меню водителя"""
    while True:
        print("\n" + "="*50)
        print(f"   ДОБРО ПОЖАЛОВАТЬ, {user.name.upper()}!")
        print("          МЕНЮ ВОДИТЕЛЯ")
        print("="*50)
        print("1.Доступные заказы")
        print("2.Мои активные заказы")
        print("3.Завершенные заказы")
        print("4.Мой профиль")
        print("5.Сменить статус (Свободен/Занят)")
        print("0.Выйти из аккаунта")
        print("-"*50)
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            available_order = show_available_orders(user.id)
            if available_order:
                accept_order(available_order, user.id)
        
        elif choice == "2":
            active_order = show_my_active_orders(user.id)
            if active_order:
                manage_active_order(active_order, user.id)
        
        elif choice == "3":
            show_completed_orders(user.id)
        
        elif choice == "4":
            show_driver_profile(user.id)
        
        elif choice == "5":
            from driver import get_driver_by_user_id
            driver_info = get_driver_by_user_id(user.id)
            if driver_info:
                new_status = not driver_info.is_available
                driver_info.set_available(new_status)
                status_text = "Свободен" if new_status else "Занят"
                print(f"Статус изменен на: {status_text}")
        
        elif choice == "0":
            print(f"\nДо свидания, {user.name}!")
            break
        else:
            print("\nНеверный ввод")