import socketserver
import time
import re


def sigma(): #TODO
    return 1


def run_operations(client_message):
    li = re.findall(r"[\w]+", client_message)
    if li[1] == 'oper' and li[2] == 'dodawanie' and li[3] == 'stat' and li[5] == li[7] == li[9] == 'numb':
        result = int(li[6]) + int(li[8]) + int(li[10])
        return 'Wynikiem operacji jest %s' % result

    elif li[1] == 'oper' and li[2] == 'mnozenie' and li[3] == 'stat' and li[5] == li[7] == li[9] == 'numb':
        result = int(li[6]) * int(li[8]) * int(li[10])
        return 'Wynikiem operacji jest %s' % result

    elif li[1] == 'oper' and li[2] == 'odejmowanie' and li[3] == 'stat' and li[5] == li[7] == li[9] == 'numb':
        result = int(li[6]) - int(li[8]) - int(li[10])
        return 'Wynikiem operacji jest %s' % result

    elif li[1] == 'oper' and li[2] == 'dzielenie' and li[3] == 'stat' and li[5] == li[7] == li[9] == 'numb':
        result = int(li[6]) / int(li[8]) / int(li[10])
        return 'Wynikiem operacji jest %s' % result

    elif li[0] == 'sumowanie':
        result = sigma()
        return 'Wynikiem operacji jest %s' % result

    else:
        return 'Niepoprawny naglowek!'


class UDP(socketserver.BaseRequestHandler):
    def handle(self):
        msg_from_client = self.request[0].strip()
        socket = self.request[1]
        client_add = self.client_address[0]

        if msg_from_client.decode() == 'terminate':
            print("ZDALNE ZAMKNIECIE SERWERA PRZEZ KLIENTA")
            exit(0)

        else:
            print("Wiadomość od", client_add, ":", msg_from_client.decode())

        server_response = run_operations(str(msg_from_client))
        socket.sendto(server_response.encode(), self.client_address)


if __name__ == "__main__":
    server_address = ('127.0.0.1', 15200)
    server_UDP = socketserver.UDPServer(server_address, UDP)
    server_UDP.serve_forever(0.5)

