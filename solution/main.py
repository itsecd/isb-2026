import sys
import argparse
from hmac_logic import create_hmac, verify_hmac
from send_and_receive import send_message, receive_message
from PyQt6.QtWidgets import QApplication

from ui import MainWindow 

def parser():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = False)
    group.add_argument('-gen','--generation',action='store_true', help='Запускает режим генерации подписи(key_path/data_path)')
    group.add_argument('-send','--send',action='store_true',help='Запускает режим отправки подписанного сообщения(data_path/hmac_path/send_path)')
    group.add_argument('-rec','--receive',action='store_true',help='Запускает режим получения и проверки сообщения(key/message_path)')
    parser.add_argument('arg1', nargs='?', help='Смотреть в help')
    parser.add_argument('arg2', nargs='?', help='Смотреть в help')
    parser.add_argument('arg3', nargs='?', help='Путь отправки(только для send)')
    args = parser.parse_args()
    return args

def main():
    action = parser()
    arg1 = action.arg1
    arg2 = action.arg2
    arg3 = action.arg3
    match action:
        case _ if action.generation:
            match arg1:
                case None:
                    print("generation needs 2 positional arguments")
                    return
            match arg2:
                case None:
                    print("generation needs 2 positional arguments")
                    return
            print(create_hmac(arg1, arg2))
        case _ if action.send:
            match arg1:
                case None:
                    print("send needs 3 positional arguments")
                    return
            match arg2:
                case None:
                    print("send needs 3 positional arguments")
                    return
            match arg3:
                case None:
                    print("send needs 3 positional arguments")
                    return
            send_message(arg1, arg2, arg3)
        case _ if action.receive:
            match arg1:
                case None:
                    print("receive needs 2 positional argument")
                    return
            match arg2:
                case None:
                    print("receive needs 2 positional argument")
                    return
            valid, data = receive_message(arg1, arg2)
            match valid:
                case True:
                    print("Data is valid")
                    print(data)
                case False:
                    print("Data was broken")
        case _ if not (action.generation or action.send or action.receive):
            app = QApplication(sys.argv)
            window = MainWindow()
            window.show()
            sys.exit(app.exec())

if __name__ == "__main__":
    main()