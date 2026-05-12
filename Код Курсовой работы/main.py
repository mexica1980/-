from database import initialize_db, add_test_data
from menu import main_menu

def main():
    """Главная функция приложения"""
    print("\n" + "="*60)
    print("   СЛУЖБА ТАКСИ - СИСТЕМА УЧЕТА ЗАКАЗОВ")
    print("="*60)
    
    # Инициализируем базу данных
    initialize_db()
    add_test_data()
    
    print("\n Система готова к работе")
    print("="*60)
    
    # Запускаем главное меню
    main_menu()

if __name__ == "__main__":
    main()