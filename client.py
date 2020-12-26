import socket
from sys import argv

client_socket = socket.socket()
host = '127.0.0.1'
# port = int(argv[1])
port = 8080

print('Waiting for connection response')
try:
    client_socket.connect((host, port))
except socket.error as e:
    print(str(e))

res = client_socket.recv(1024)
while True:
    Input = input('Request: ')
    client_socket.send(str.encode(Input))
    res = client_socket.recv(1024)
    print(res.decode('utf-8'))

client_socket.close()
