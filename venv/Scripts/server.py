import socketserver
import time
import re
session_number = -1 # -1 PONIEWAŻ PRZED NADANIEM ID SESJI ZWIĘKSZA JĄ O 1 (WIĘC ZACZYNAMY OD 0)
given_list = []


def sigma(given_num, ssid):  # SUMOWANIE
    try:
        given_num = int(given_num)
    except ValueError:
        print("BŁĄD WARTOŚCI")
        return given_list[int(ssid)]
    given_list[int(ssid)] += given_num
    return given_list[int(ssid)]


def run_operations(client_message): # TWORZY ODPOWIEDŹ DLA ODPOWIEDNIEJ OPERACJI, JEŻELI NIE MA NUMERU SESJI
                                    # PROGRAM PRZYPISUJE JĄ DLA KLIENTA I ZWIĘKSZA O 1 ABY NADAĆ NASTĘPNEMU
    global session_number
    li = re.findall(r"[\w]+", client_message)
    if li[1] == 'oper' and li[2] == 'dodawanie' and li[3] == 'stat' and li[5] == li[7] == li[9] == 'numb': # DODAWANIE
        if li[14] == "null":
            session_number += 1
            li[14] = session_number
        result = int(li[6]) + int(li[8]) + int(li[10])
        czas = li[12]
        return 'oper#dodawanie@stat#ok@numb#%s@time#%s@iden#%s@' % (result, czas, session_number)

    elif li[1] == 'oper' and li[2] == 'mnozenie' and li[3] == 'stat' and li[5] == li[7] == li[9] == 'numb': # MNOŻENIE
        if li[14] == "null":
            session_number += 1
            li[14] = session_number
        result = int(li[6]) * int(li[8]) * int(li[10])
        czas = li[12]
        return 'oper#mnozenie@stat#ok@numb#%s@time#%s@iden#%s@' % (result, czas, session_number)

    elif li[1] == 'oper' and li[2] == 'odejmowanie' and li[3] == 'stat' and li[5] == li[7] == li[9] == 'numb': # ODEJMOWANIE
        if li[14] == "null":
            session_number += 1
            li[14] = session_number
        result = int(li[6]) - int(li[8]) - int(li[10])
        czas = li[12]
        return 'oper#odejmowanie@stat#ok@numb#%s@time#%s@iden#%s@' % (result, czas, session_number)

    elif li[1] == 'oper' and li[2] == 'dzielenie' and li[3] == 'stat' and li[5] == li[7] == li[9] == 'numb': # DZIELENIE
        if li[14] == "null":
            session_number += 1
            li[14] = session_number
        try:
            result = int(li[6]) / int(li[8]) / int(li[10])
        except ZeroDivisionError:
            result = 'Błąd'
        czas = li[12]
        return 'oper#dzielenie@stat#ok@numb#%s@time#%s@iden#%s@' % (result, czas, session_number)

    elif li[1] == 'oper' and li[2] == 'sumowanie' and li[3] == 'stat' and li[5] == 'numb': # SUMOWANIE
        if li[10] == "null":
            session_number += 1
            li[10] = session_number
        result = sigma(li[6], li[10])
        czas = li[8]
        return 'oper#sumowanie@stat#ok@numb#%s@time#%s@iden#%s@' % (result, czas, session_number)

    elif li[1] == 'oper' and li[2] == 'endsumowanie': # KONIEC SUMOWANIA
        if li[8] == "null":
            session_number += 1
            li[8] = session_number
        result = sigma(0, li[8])
        given_list[int(li[8])] = 0
        czas = li[6]
        return 'oper#endsumowanie@stat#ok@numb#%s@time#%s@iden#%s@' % (result, czas, session_number)

    elif li[1] == 'oper' and li[2] == 'null' and li[3] == 'stat' and li[5] == li[7] == li[9] == 'numb': # BŁĄD
        if li[14] == "null":
            session_number += 1
            li[14] = session_number
        czas = li[12]
        return 'oper#null@stat#fail@numb#0@time#%s@iden#%s@' % (czas, session_number)

    else:
        return 'oper#null@stat#fail@numb#0@time#%s@iden#%s@' % (czas, session_number) # BŁĄD OGÓLNY


class UDP(socketserver.BaseRequestHandler):
    def handle(self):
        msg_from_client = self.request[0].strip() # ROZKODOWANIE WIADOMOŚCI
        socket = self.request[1]
        client_add = self.client_address[0] # ROZKODOWANIE ADRESU KLIENTA

        if msg_from_client.decode() == 'terminate': # ZDALNE ZAKOŃCZENIE DZIAŁANIA SERWERA
            print("ZDALNE ZAMKNIECIE SERWERA PRZEZ KLIENTA")
            exit(0)

        else:
            print("Wiadomość od", client_add, ":", msg_from_client.decode()) # DRUKUJE WIADOMOŚĆ JEŚLI NIE JEST TERMINATE

        server_response = run_operations(str(msg_from_client)) # WYSYŁA ODPOWIEDŹ DLA ODPOWIEDNIEJ OPERACJI
        socket.sendto(server_response.encode(), self.client_address)


if __name__ == "__main__":

    # ZAPELNIA LISTE SUMOWANIA, ZEBY NIE BYLA PUSTA NP
    # JEZELI SESJA 2 CHCE SUMOWANIE, A 0 I 1 NIE UZYWALO (INDEX ERROR)
    for x in range(10):
        given_list.append(0)

    server_address = (input("Wprowadź IP serwera: "), 15200)
    server_UDP = socketserver.UDPServer(server_address, UDP)
    server_UDP.serve_forever(0.5)