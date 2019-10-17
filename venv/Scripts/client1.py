import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind = (('', 15200))
buffer_size = 4096
m = sock.recvfrom(buffer_size)
server_address = m[1]


while True:
    bytesToSend = input('Wprowadz liczbe: ')
    sock.sendto(bytesToSend.encode(), server_address)

    try:
        msgFromServer = sock.recvfrom(buffer_size)
    except ConnectionResetError:
        print('Nie udało się połączyć z serwerem :(')
        exit()

    msg = ('Odpowiedz od serwera: ', msgFromServer[0])
    print(msg)