import socket
from _thread import *
import functions
import threading

lock = threading.Lock()  # creating thread for every request

valid_methods = ['POST', 'UPDATE', 'DELETE', 'HEAD', 'PUT', 'PATCH']


def multi_threaded_client(connection):
    req = connection.recv(1024)  # 10240  byte request received
    request = req.decode('utf-8')
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

    lock.release()  # thread unlocked
    connection.close()  # connection closed


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '0.0.0.0'
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
    lock.acquire()
    start_new_thread(multi_threaded_client, (client,))
    numOfThread += 1
    print('Thread Number: ' + str(numOfThread))
server_socket.close()
