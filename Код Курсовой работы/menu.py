from menu_auth import show_auth_menu
from menu_client import menu_client
from menu_driver import menu_driver
from menu_admin import menu_admin

def route_by_role(user):
    """Маршрутизация по роли пользователя"""
    if user is None:
        return False
    
    if user.role == 'client':
        menu_client(user)
    elif user.role == 'driver':
        menu_driver(user)
    elif user.role == 'admin':
        menu_admin(user)
    else:
        print(f"Неизвестная роль: {user.role}")
        return False
    
    return True

def main_menu():
    """Главное меню приложения"""
    while True:
        user = show_auth_menu()
        
        if user is None:
            print("\n До свидания!")
            break
        
        route_by_role(user)