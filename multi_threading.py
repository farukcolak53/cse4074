import socket
from _thread import *
from sys import argv
import functions
import threading

lock = threading.Lock()  # creating thread for every request

valid_methods = ['POST', 'UPDATE', 'DELETE', 'PUT', 'PATCH']  # Some Valid but Not Implemented Methods


def multi_threaded_client(connection):
    req = connection.recv(1024)  # 1024  byte request received
    request = req.decode('utf-8')
    if request:  # If request is not empty
        split_words = request.split("\n")
        method = split_words[0].split()[0]  # Parse the method (GET etc.)
        size = split_words[0].split()[1].replace("/", "")  # Parse the size of the requested document

        print("----------------------------")
        print("---------Request------------")
        print(request)
        print("----------------------------")

        if method == 'GET' and size.isdigit():
            size = int(size)
            if 100 <= size <= 20000:
                filename = "files/" + str(size) + ".html"
                functions.create_requested_document(size)
                functions.generate_response_html(filename, connection, size)
            else:
                filename = "400.html"
                functions.generate_response_html(filename, connection, 0)
        else:  # If the method is not GET or size is not digit
            if method in valid_methods:
                filename = "501.html"
                functions.generate_response_html(filename, connection, 0)
            elif method == 'HEAD':  # HEAD needs empty body for valid response
                filename = '501.html'
                functions.generate_response_for_head(filename, connection)
            else:
                filename = "400.html"
                functions.generate_response_html(filename, connection, 0)
        print("-------------------------------------")

    lock.release()  # thread unlocked
    connection.close()  # connection closed


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '127.0.0.1'
port = int(argv[1])

numOfThread = 0

try:
    server_socket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Server socket is listening..')

server_socket.listen(10)

while True:
    client, address = server_socket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    lock.acquire()
    start_new_thread(multi_threaded_client, (client,))
    numOfThread += 1
    print('Thread Number: ' + str(numOfThread))
server_socket.close()
