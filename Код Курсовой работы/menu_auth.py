from user import User, authenticate, get_user_by_login

def register():
    """Регистрация нового пользователя"""
    print("\n" + "="*50)
    print("           РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ")
    print("="*50)
    
    login = input("Придумайте логин: ")
    if get_user_by_login(login):
        print(" Такой логин уже существует!")
        return None
    
    password = input("Придумайте пароль: ")
    password2 = input("Повторите пароль: ")
    
    if password != password2:
        print(" Пароли не совпадают!")
        return None
    
    name = input("Ваше имя: ")
    phone = input("Номер телефона: ")
    
    print("\nВыберите роль:")
    print("1.Клиент")
    print("2.Водитель")
    role_choice = input("Ваш выбор (1-2): ")
    
    role = 'client' if role_choice == '1' else 'driver' if role_choice == '2' else 'client'
    
    user = User(login=login, password=password, name=name, phone=phone, role=role)
    user.save()
    
    print(f"\nРегистрация успешна! Вы вошли как {name} ({role})")
    return user

def login():
    """Вход в систему"""
    print("\n" + "="*50)
    print("              ВХОД В СИСТЕМУ ТАКСИ")
    print("="*50)
    
    login_input = input("Логин: ")
    password_input = input("Пароль: ")
    
    user = authenticate(login_input, password_input)
    
    if user:
        print(f"\n Добро пожаловать, {user.name}!")
        print(f"Роль: {user.role}")
        return user
    else:
        print("\n Неверный логин или пароль!")
        return None

def show_auth_menu():
    """Показывает меню входа/регистрации"""
    print("\n" + "="*50)
    print("          ДОБРО ПОЖАЛОВАТЬ В СЛУЖБУ ТАКСИ")
    print("="*50)
    print("1.Вход")
    print("2.Регистрация")
    print("0.Выход")
    print("-"*50)
    
    choice = input("Выберите действие: ")
    
    if choice == "1":
        return login()
    elif choice == "2":
        return register()
    elif choice == "0":
        return None
    else:
        print("Неверный выбор")
        return show_auth_menu()