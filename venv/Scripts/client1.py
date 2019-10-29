import socket
import re
import time

def encode_msg(user_input):
    li = re.findall(r"[\w]+", user_input)
    try:
        if li[0].isnumeric():
            message = ["oper", '#', 'sum_add', '@', "stat", '#', "null", '@', 'numb', '#', li[0], '@', 'time', '#',
                       str(int(time.time())), '@']
        elif li[0] == "koniecsumowania":
            message = ["oper", '#', li[0], '@', "stat", '#', "null", '@', 'time', '#', str(int(time.time())), '@']

        elif li[0] == "sumowanie":
            message = ["oper", '#', li[0], '@', "stat", '#', "null", '@', 'numb', '#', li[1], '@', 'time', '#',
                       str(int(time.time())), '@']

        elif li[0] == "dodawanie" or "odejmowanie" or "mnozenie" or "dzielenie":
            message = ["oper", '#', li[0], '@', "stat", '#', "null", '@', 'numb', '#', li[1], '@', 'numb', '#', li[2],
                       '@','numb', '#', li[3], '@', 'time', '#', str(int(time.time())), '@']

    except IndexError:
        # musi byc w formatce #@ zeby nie wywalalo - jako operacja: lipens
        message = ["oper", '#', 'lipens', '@', "stat", '#', "null", '@', 'numb', '#', '0', '@', 'numb', '#', '0', '@',
                   'numb', '#', '0', '@', 'time', '#', str(int(time.time())), '@']
    message = ''.join(message)
    return message


def decode_message(server_answer):
    li = re.findall(r"[\w]+", server_answer)
    if li[1] == 'lipa':
        return "Niepoprawny nagłówek"
    else:
        return "Wynikiem operacji " + li[1] + " jest: " + li[5]



def print_help():
    print('"dodawanie" [liczba1] [liczba2] [liczba3] - serwer oblicza sumę trzech liczb\n'
          '"odejmowanie" [liczba1] [liczba2] [liczba3] - serwer oblicza różnicę trzech liczb\n'
          '"mnozenie" [liczba1] [liczba2] [liczba3] - serwer oblicza iloczyn trzech liczb\n'
          '"dzielenie" [liczba1] [liczba2] [liczba3] - serwer oblicza iloraz trzech liczb\n'
          '"exit" - zakończenie programu klienta\n'
          '"terminate" - zdalne wyłączenie serwera')


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # server_address = ('127.0.0.1', 15200)
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

            decoded  = decode_message(server_response[0].decode())
            print("\nOdpowiedź od serwera :", decoded)

           # print("\nOdpowiedź od serwera :", server_response[0].decode()) - poprzednia opcja

        except socket.timeout:
            print("Serwer nie odpowiedział, sprawdź połączenie")
