import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.8.112', 5000)
buffer_size = 4096


while True:

    bytesToSend = input('Wprowadz liczbe: ')

    if(bytesToSend == 69420):
        exit()

    sock.sendto(bytesToSend.encode(), server_address)

    msgFromServer = sock.recvfrom(buffer_size)

    msg = ('Odpowiedz od serwera: ', msgFromServer[0])
    print(msg)