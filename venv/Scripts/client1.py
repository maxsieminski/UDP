import socket
import re
import time
def encode_msg(user_input):
    li = re.findall(r"[\w]+", user_input)
    message = ["oper", '#', li[0], '@', "stat", '#', "null", '@', 'numb', '#', li[1], '@', 'numb', '#', li[2], '@',
               'numb', '#', li[3], '@', 'time', '#', str(int(time.time())), '@']
    message = ''.join(message)
    return message


def print_help():
    print('"dodawanie" [liczba1] [liczba2] [liczba3] - serwer oblicza sumę trzech liczb\n'
          '"odejmowanie" [liczba1] [liczba2] [liczba3] - serwer oblicza różnicę trzech liczb\n'
          '"mnozenie" [liczba1] [liczba2] [liczba3] - serwer oblicza iloczyn trzech liczb\n'
          '"dzielenie" [liczba1] [liczba2] [liczba3] - serwer oblicza iloraz trzech liczb\n'
          '"exit" - zakończenie programu klienta\n'
          '"terminate" - zdalne wyłączenie serwera')


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 15200)
    client.settimeout(5)

    while True:
        message = input("\nWariant 19 - model komunikacji n <-> 1, wprowadź komendę, lub wpisz help\nWprowadź komendę:")

        if message == 'help':
            print_help()
            continue

        elif message == 'exit':
            exit(0)

        elif message == 'terminate':
            client.sendto(message.encode(), server_address)
            print("Wylaczono serwer\nWyłączanie klienta...")
            exit(0)

        else:
            print("Wysylam...", end='')
            client.sendto(encode_msg(message).encode(), server_address)
            print("...", end='')

        try:
            server_response = client.recvfrom(1024)
            print("\nOdpowiedź od serwera :", server_response[0].decode())
        except socket.timeout:
            print("Serwer nie odpowiedział, sprawdź połączenie")
