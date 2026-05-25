from file_open_and_close import *
from salt_generation import *
from hash_generation import *
from hash_comparison import *

def user_registration(config_path: str):
    """
    Регистрирует пользователя в программе
    Args:
        config_path (str): Путь к файлу конфигурации.
    Returns:
        None: Функция ничего не возвращает, только выполняет действие.
    """
    config=load_config(config_path)
    db_path = config.get("files", {}).get("data_base", "data_base.json")
    data_base= load_user_database(db_path)

    user_name=""
    while user_name=="":
        current_input=input("Please, enter your username: ").strip()
        if current_input == "":
            print("No username was entred. Please, try again.")
            continue
        if current_input in data_base:
            print("Username is already taken. Please, enter another.")
            continue
        user_name = current_input
     
    user_password=""
    while user_password=="":
        current_password=input("Please, enter your password: ").strip()
        if current_password == "":
            print("No password was entred. Please, try again.") 
            continue
        user_password = current_password

    user_salt = generate_salt()
   
    hash= hash_password(user_password, user_salt)

    add_user_to_file(db_path, user_name, hash, user_salt)

    print("Registration is complete! Now please log in.")


def user_login(config_path: str)->bool:
    """
    Логинит пользователя в программе
    Args:
        config_path (str): Путь к файлу конфигурации.
    Returns:
        Bool: True/False в зависимости от успошности входа
    """
    config=load_config(config_path)
    db_path = config.get("files", {}).get("data_base", "data_base.json")
    data_base= load_user_database(db_path)

    user_name=""
    while user_name=="":
        current_input=input("Please, enter your username: ").strip()
        if current_input == "":
            print("No username was entred. Please, try again.")
            continue
        user_name = current_input
     
    user_password=""
    while user_password=="":
        current_password=input("Please, enter your password: ").strip()
        if current_password == "":
            print("No password was entred. Please, try again.") 
            continue
        user_password = current_password

    checking_result=hash_comparison(data_base, user_name, user_password)
    if checking_result==True:
        print("Logginig in has been successful. Congrats")
        return True
    else:
        print("Password is incorrect, please try again.")
        return False


    

