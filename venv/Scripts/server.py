import socket
import select # TODO : OGARNAC W JAKI SPOSOB ROBI TIMEOUT DLA NASLUCHU
import time
import re


def sigma(): #TODO
    return 1


def run_operations(client_message):
    li = re.findall(r"[\w]+", client_message)
    print(li)

    if li[0] == 'oper' and li[1] == 'dodawanie' and li[2] == 'stat'  and li[4] == li[6] == li[8] == 'numb':
        result = int(li[5]) + int(li[7]) + int(li[9])
        return 'Wynikiem operacji jest %s' %result

    elif li[0] == 'oper' and li[1] == 'mnozenie' and li[2] == 'stat' and li[4] == li[6] == li[8] == 'numb':
        result = int(li[5]) * int(li[7]) * int(li[9])
        return 'Wynikiem operacji jest %s' % result

    elif li[0] == 'oper' and li[1] == 'odejmowanie' and li[2] == 'stat' and li[4] == li[6] == li[8] == 'numb':
        result = int(li[5]) - int(li[7]) - int(li[9])
        return 'Wynikiem operacji jest %s' % result

    elif li[0] == 'oper' and li[1] == 'dzielenie' and li[2] == 'stat' and li[4] == li[6] == li[8] == 'numb':
        result = int(li[5]) / int(li[7]) / int(li[9])
        return 'Wynikiem operacji jest %s' % result

    elif li[0] == 'sumowanie':
        result = sigma()
        return 'Wynikiem operacji jest %s' % result

    else:
        return 'Niepoprawny naglowek!'


def broadcast():
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(''.encode(), ('255.255.255.255', 15200))


def receive_comm():
    sock.setblocking(0) # PATRZ IMPORT SELECT
    ready = select.select([sock], [], [], 5) # PATRZ IMPORT SELECT
    if ready[0]: # PATRZ IMPORT SELECT
        client_input = sock.recvfrom(buffer_size)
        client_message = client_input[0].decode()
        client_address = client_input[1]
        print('Wiadomosc od klienta ', client_address, ' : ', client_message)
        server_response = run_operations(client_message)
        sock.sendto(server_response.encode(), client_address)


# Tworzy gniazdo UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0], 15201)
buffer_size = 4096
print('Uruchamiam %s na porcie %s' % server_address)

while True:
    broadcast()
    receive_comm()
