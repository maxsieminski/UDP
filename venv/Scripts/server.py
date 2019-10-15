import socket

# Tworzy gniazdo UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.8.112', 5000)
buffer_size = 4096

print('Uruchamiam %s na porice %s' % server_address)
sock.bind(server_address)

while True:
    #oczekuje na odpowiedz klienta
    client_input = sock.recvfrom(buffer_size)
    client_message = client_input[0].decode()
    client_address = client_input[1]
    print('Wiadomosc od klienta ', client_address, ' : ', client_message)

    server_response = ('Otrzymano wiadomosc : ' + client_message)
    sock.sendto(server_response.encode(), client_address)