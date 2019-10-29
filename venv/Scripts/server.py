import socketserver
import time
import re

given_list = []
def sigma(given_num):
    given_num = int(given_num)
    given_list.append(given_num)
    print(given_list[0])
    suma = sum(given_list)

    return suma


def run_operations(client_message):
    li = re.findall(r"[\w]+", client_message)
    if li[1] == 'oper' and li[2] == 'dodawanie' and li[3] == 'stat' and li[5] == li[7] == li[9] == 'numb':
        result = int(li[6]) + int(li[8]) + int(li[10])
        return 'oper#dodawanie@stat#ok@numb#%s@' % result

    elif li[1] == 'oper' and li[2] == 'mnozenie' and li[3] == 'stat' and li[5] == li[7] == li[9] == 'numb':
        result = int(li[6]) * int(li[8]) * int(li[10])
        return 'oper#mnozenie@stat#ok@numb#%s@' % result

    elif li[1] == 'oper' and li[2] == 'odejmowanie' and li[3] == 'stat' and li[5] == li[7] == li[9] == 'numb':
        result = int(li[6]) - int(li[8]) - int(li[10])
        return 'oper#odejmowanie@stat#ok@numb#%s@' % result

    elif li[1] == 'oper' and li[2] == 'dzielenie' and li[3] == 'stat' and li[5] == li[7] == li[9] == 'numb':
        result = int(li[6]) / int(li[8]) / int(li[10])
        return 'oper#dzielenie@stat#ok@numb#%s@' % result

    elif li[1] == 'oper' and li[2] == 'sumowanie' and li[3] == 'stat' and li[5] == 'numb':
        result = sigma(li[6])
        return 'oper#sumowania@stat#ok@numb#%s@' % result

    elif li[1] == 'oper' and li[2] == 'sum_add' and li[3] == 'stat' and li[5] == 'numb':
        result = sigma(li[6])
        return 'oper#sumowania@stat#ok@numb#%s@' % result

    elif li[1] == 'oper' and li[2] == 'koniecsumowania':
        result = sigma(0)
        given_list.clear()
        return 'oper#koniecsumowania@stat#ok@numb#%s@' % result

    elif li[1] == 'oper' and li[2] == 'lipa' and li[3] == 'stat' and li[5] == li[7] == li[9] == 'numb':
        return 'oper#lipa@stat#ok@numb#0@'

    else:
        return 'oper#lipa@stat#ok@numb#0@'


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
    server_address = ('172.20.10.4', 15200)
    server_UDP = socketserver.UDPServer(server_address, UDP)
    server_UDP.serve_forever(0.5)

