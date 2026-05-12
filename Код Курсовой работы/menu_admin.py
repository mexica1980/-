from user import get_all_users, get_user_by_id, User, get_users_by_role
from driver import get_all_drivers, get_driver_by_user_id, Driver
from order import get_all_orders, get_active_orders
from car import get_car_by_driver_id, Car

def show_all_users():
    """Показать всех пользователей"""
    users = get_all_users()
    
    if not users:
        print("\n Нет пользователей")
        return
    
    print("\n" + "="*70)
    print("                    ВСЕ ПОЛЬЗОВАТЕЛИ")
    print("="*70)
    
    role_ru = {'client': 'Клиент', 'driver': 'Водитель', 'admin': 'Админ'}
    
    for u in users:
        print(f"\n ID: {u.id}")
        print(f"    {u.name} | @{u.login}")
        print(f"    {u.phone}")
        print(f"    {role_ru.get(u.role, u.role)}")
        print(f"    {u.created_date[:16]}")
    
    print("\n" + "="*70)
    input("Нажмите Enter для продолжения...")

def show_all_orders():
    """Показать все заказы"""
    orders = get_all_orders()
    
    if not orders:
        print("\n Нет заказов")
        return
    
    print("\n" + "="*70)
    print("                    ВСЕ ЗАКАЗЫ")
    print("="*70)
    
    status_ru = {
        'waiting': ' Ожидает',
        'accepted': ' Принят',
        'in_progress': ' В пути',
        'completed': ' Завершен',
        'cancelled': ' Отменен'
    }
    
    total_income = sum(o.price for o in orders if o.status == 'completed')
    
    for o in orders:
        client = get_user_by_id(o.client_id)
        client_name = client.name if client else "N/A"
        
        print(f"\n #{o.id} | {status_ru.get(o.status, o.status)} | {o.created_date[:16]}")
        print(f"    Клиент: {client_name}")
        print(f"    {o.from_address[:30]} → {o.to_address[:30]}")
        print(f"    {o.price} руб.")
        
        if o.driver_id:
            driver = get_user_by_id(o.driver_id)
            driver_name = driver.name if driver else "N/A"
            print(f"    Водитель: {driver_name}")
    
    print("\n" + "="*70)
    print(f" ОБЩИЙ ДОХОД (завершенные): {total_income} руб.")
    print(f" ВСЕГО ЗАКАЗОВ: {len(orders)}")
    print("="*70)
    input("Нажмите Enter для продолжения...")

def show_statistics():
    """Показать общую статистику системы"""
    users = get_all_users()
    drivers = get_all_drivers()
    orders = get_all_orders()
    active_orders = get_active_orders()
    
    completed_orders = [o for o in orders if o.status == 'completed']
    cancelled_orders = [o for o in orders if o.status == 'cancelled']
    
    total_income = sum(o.price for o in completed_orders)
    
    # Рейтинг водителей
    driver_ratings = [(d, get_user_by_id(d.user_id)) for d in drivers]
    driver_ratings.sort(key=lambda x: x[0].rating, reverse=True)
    
    print("\n" + "="*60)
    print("              СТАТИСТИКА СИСТЕМЫ ТАКСИ")
    print("="*60)
    
    print("\n ПОЛЬЗОВАТЕЛИ:")
    print(f"Всего: {len(users)}")
    print(f"Клиенты: {len([u for u in users if u.role == 'client'])}")
    print(f"Водители: {len([u for u in users if u.role == 'driver'])}")
    print(f"Админы: {len([u for u in users if u.role == 'admin'])}")
    
    print("\n ЗАКАЗЫ:")
    print(f"Всего: {len(orders)}")
    print(f"Завершено: {len(completed_orders)}")
    print(f"Отменено: {len(cancelled_orders)}")
    print(f"Активных: {len(active_orders)}")
    print(f"Общий доход: {total_income} руб.")
    
    if completed_orders:
        avg_price = total_income / len(completed_orders)
        print(f"   Средний чек: {avg_price:.2f} руб.")
    
    print("\n ТОП-3 ВОДИТЕЛЯ ПО РЕЙТИНГУ:")
    for i, (d, user) in enumerate(driver_ratings[:3], 1):
        if user:
            print(f"   {i}. {user.name} — {d.rating}/5 ({d.experience_years} лет опыта)")
    
    print("\n" + "="*60)
    input("Нажмите Enter для продолжения...")

def add_driver():
    """Добавить нового водителя (администратор)"""
    print("\n" + "="*50)
    print("           ДОБАВЛЕНИЕ ВОДИТЕЛЯ")
    print("="*50)
    
    login = input("Логин: ")
    from user import get_user_by_login
    if get_user_by_login(login):
        print("Логин уже существует!")
        return
    
    password = input("Пароль: ")
    name = input("Имя: ")
    phone = input("Телефон: ")
    license_number = input("Номер водительского удостоверения: ")
    
    try:
        experience = int(input("Опыт работы (лет): "))
    except ValueError:
        experience = 0
    
    from datetime import datetime
    user = User(
        login=login,
        password=password,
        name=name,
        phone=phone,
        role='driver',
        created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    user.save()
    
    driver = Driver(
        user_id=user.id,
        license_number=license_number,
        experience_years=experience,
        rating=5.0,
        is_available=True
    )
    driver.save()
    
    print(f"\n Водитель {name} добавлен!")
    print(f"   Логин: {login}, Пароль: {password}")

def delete_user():
    """Удалить пользователя"""
    users = get_all_users()
    
    print("\n" + "="*50)
    print("           УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ")
    print("="*50)
    
    for u in users:
        print(f"  {u.id}. {u.name} ({u.login}) - {u.role}")
    
    try:
        user_id = int(input("\nВведите ID пользователя для удаления: "))
        user = get_user_by_id(user_id)
        
        if user:
            if user.role == 'admin':
                print("Нельзя удалить администратора")
                return
            
            confirm = input(f"Удалить {user.name}? (да/нет): ")
            if confirm.lower() in ['да', 'yes', 'д', 'y']:
                user.delete()
                print(f"Пользователь {user.name} удален")
        else:
            print("Пользователь не найден")
    except ValueError:
        print(" Неверный ID")

def menu_admin(user):
    """Главное меню администратора"""
    while True:
        print("\n" + "="*50)
        print(f"   ДОБРО ПОЖАЛОВАТЬ, АДМИНИСТРАТОР {user.name.upper()}!")
        print("          МЕНЮ АДМИНИСТРАТОРА")
        print("="*50)
        print("1.Все пользователи")
        print("2.Все заказы")
        print("3.Статистика")
        print("4.Добавить водителя")
        print("5.Удалить пользователя")
        print("6.Мой профиль")
        print("0.Выйти из аккаунта")
        print("-"*50)
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            show_all_users()
        elif choice == "2":
            show_all_orders()
        elif choice == "3":
            show_statistics()
        elif choice == "4":
            add_driver()
        elif choice == "5":
            delete_user()
        elif choice == "6":
            print("\n" + "="*50)
            print("           ПРОФИЛЬ АДМИНИСТРАТОРА")
            print("="*50)
            print(f"Имя: {user.name}")
            print(f"Телефон: {user.phone}")
            print(f"Логин: {user.login}")
            print(f"Роль: {user.role}")
            print(f"Дата регистрации: {user.created_date[:16]}")
            input("\n Нажмите Enter для продолжения...")
        elif choice == "0":
            print(f"\nДо свидания, {user.name}!")
            break
        else:
            print("\nНеверный ввод")