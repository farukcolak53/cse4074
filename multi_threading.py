import socket
from _thread import *
from sys import argv

valid_methods = ['POST', 'UPDATE', 'DELETE', 'HEAD', 'PUT', 'PATCH']


def create_html(filename, size):
    file = open(filename, 'w')

    message = """
    <html>
        <head></head>
        <body><p>Hello World!</p></body>
    </html>"""

    file.write(message)
    file.close()

    return filename


def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:

        request = connection.recv(2048)
        request = request.decode('utf-8')
        split_words = str(request).split()
        method = split_words[0]
        size = int(split_words[1].replace("/", ""))

        if method == 'GET' and 100 <= size <= 20000:
            filename = str(size) + ".html"
            response = "http://localhost:8080/" + str(create_html(filename, size))
        else:
            if method in valid_methods:
                response = 'Not Implemented (501)'
            else:
                response = 'Bad Request (400)'

        if not request:
            break
        connection.sendall(str.encode(response))
    connection.close()


server_socket = socket.socket()
host = '127.0.0.1'
# port = int(argv[1])
port = 8080

numOfThread = 0

try:
    server_socket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')

server_socket.listen(5)  # TODO: what is ?

while True:
    client, address = server_socket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (client,))
    numOfThread += 1
    print('Thread Number: ' + str(numOfThread))
server_socket.close()
