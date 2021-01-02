import socket
from _thread import *
import functions

valid_methods = ['POST', 'UPDATE', 'DELETE', 'HEAD', 'PUT', 'PATCH']


def multi_threaded_client(connection):
    while True:
        request = connection.recv(2048)
        if not request:
            break
        request = request.decode('utf-8')
        split_words = request.split("\n")
        method = split_words[0].split()[0]
        size = split_words[0].split()[1].replace("/", "")

        print("----------------------------")
        print("---------Request------------")
        print(request)
        print("----------------------------")

        if method == 'GET' and size.isdigit():
            size = int(size)
            if 100 <= size <= 20000:
                filename = "/index.html"
                functions.create_requested_document(size)
                functions.generate_response_html(filename, connection)
            else:
                filename = "400.html"
                functions.generate_response_html(filename, connection)
        else:
            if method in valid_methods:
                filename = "501.html"
                functions.generate_response_html(filename, connection)
            else:
                filename = "400.html"
                functions.generate_response_html(filename, connection)
        print("-------------------------------------")
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

print('Server socket is listening..')

server_socket.listen(5)  # TODO: what is ?

while True:
    client, address = server_socket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (client,))
    numOfThread += 1
    print('Thread Number: ' + str(numOfThread))
server_socket.close()
