import socket
import re
import time


def encode_msg(user_input, ssid):  # TWORZENIE NAGŁÓWKA DLA SERWERA
    li = re.findall(r"[\w]+", user_input)
    try:
        if li[0].isnumeric():
            message = ["oper", '#', 'suma', '@', "stat", '#', "null", '@', 'numb', '#', li[0], '@', 'time', '#',
                       str(int(time.time())), '@', "ssid", '#', ssid, '@']

        elif li[0] == "koniecsumowania":
            message = ["oper", '#', 'ends', '@', "stat", '#', "null", '@', 'time', '#', str(int(time.time())), '@',
                       "ssid", '#', ssid, '@']

        elif li[0] == "sumowanie":
            message = ["oper", '#', li[0][:4], '@', "stat", '#', "null", '@', 'numb', '#', li[1], '@', 'time', '#',
                       str(int(time.time())), '@', "ssid", '#', ssid, '@']

        elif li[0] == "dodawanie" or "odejmowanie" or "mnozenie" or "dzielenie":
            message = ["oper", '#', li[0][:4], '@', "stat", '#', "null", '@', 'numb', '#', li[1], '@', 'numb', '#', li[2],
                       '@', 'numb', '#', li[3], '@', 'time', '#', str(int(time.time())), '@', "ssid", '#', ssid, '@']

    except IndexError:  # WYSYŁA NIEPOPRAWNY NAGŁÓWEK, UŻYTKOWNIK DOSTAJE ODP NIEPOPRAWNY NAGŁÓWEK
        message = ["oper", '#', 'null', '@', "stat", '#', "fail", '@', 'numb', '#', '0', '@', 'numb', '#', '0', '@',
                   'numb', '#', '0', '@', 'time', '#', str(int(time.time())), '@', "ssid", '#', ssid, '@']
    message = ''.join(message)
    return message


def decode_message(server_answer):  # ROZKODOWANIE NAGŁÓWKA NA WIADOMOŚĆ DLA UŻYTKOWNIKA
    li = re.findall(r"[\w]+", server_answer)
    if li[1] == 'null':
        return "Niepoprawny nagłówek"
    else:
        if li[1] == "doda":
            return "Wynikiem operacji dodawania jest: " + li[5]
        elif li[1] == "odej":
            return "Wynikiem operacji odejmowania jest: " + li[5]
        elif li[1] == "mnoz":
            return "Wynikiem operacji mnozenia jest: " + li[5]
        elif li[1] == "dzie":
            return "Wynikiem operacji dzielenia jest: " + li[5]
        elif li[1] == "sumo" or li[1] == "suma":
            return "Wynikiem operacji sumowania jest: " + li[5]
        else:
            return "Wynikiem operacji sumowania jest: " + li[5] + ". Koniec sumowania."

def get_ssid(server_answer):  # UZYSKUJE NUMER SSID OD SERWERA
    li = re.findall(r"[\w]+", server_answer)
    return li[9]


def print_help():
    print('"dodawanie" [liczba1] [liczba2] [liczba3] - serwer oblicza sumę trzech liczb\n'
          '"odejmowanie" [liczba1] [liczba2] [liczba3] - serwer oblicza różnicę trzech liczb\n'
          '"mnozenie" [liczba1] [liczba2] [liczba3] - serwer oblicza iloczyn trzech liczb\n'
          '"dzielenie" [liczba1] [liczba2] [liczba3] - serwer oblicza iloraz trzech liczb\n'
          '"sumowanie" [liczba1] - wysyła liczbę do sumowania\n'
          '"[liczba1]" - wysyła liczbę do sumowania\n'
          '"koniecsumowania" - kończy sumowanie\n'
          '"exit" - zakończenie programu klienta\n'
          '"terminate" - zdalne wyłączenie serwera')


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #AF_INET - RODZINA ADRESÓW IPv4
    ssid = "null"  # DOMYŚLNY IDEN. SESJI DLA UŻYTKOWNIKA
    server_address = (input("Wprowadz IP serwera:"), 15200)

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
            client.sendto(encode_msg(message, ssid).encode(), server_address)
            print("...", end='')

        try:  # TRY Bo RECVFROM BLOKUJE JEŚLI NIE UZYSKA ODPOWIEDZI
            server_response = client.recvfrom(1024)
            if ssid == "null":  # JEŻELI NIE MASZ PRZYPISANEJ SESJI -> USTAW Z ODPOWIEDZI
                ssid = get_ssid(server_response[0].decode())
            decoded = decode_message(server_response[0].decode())
            print("\nOdpowiedź od serwera :", decoded)

        except socket.timeout:
            print("Serwer nie odpowiedział, sprawdź połączenie")