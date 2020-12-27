import socket
from _thread import *
from sys import argv
import codecs
from sys import argv, getsizeof
import random, string

valid_methods = ['POST', 'UPDATE', 'DELETE', 'HEAD', 'PUT', 'PATCH']


def write_message(size):
    str = "a"
    for i in range(size - 50):
        str = str + "a"
    return str


def random_string(string_length):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def create_html(size):
    index_file = open("./index.html", 'w+')
    body_text = str(random_string(size))
    content = "<!DOCTYPE html>\n<html>\n<head>\n"
    content += "<title>" + str(size) + " bytes</title>\n</head>\n<body>\n<p>"
    content += body_text
    content += "</p>\n</body>\n</html>"
    print("body text size: ", getsizeof(body_text))
    print("body text len: ", len(body_text))
    index_file.write(content)
    return index_file


def multi_threaded_client(connection):
    while True:
        request = connection.recv(2048)
        if not request:
            break
        request = request.decode('utf-8')
        split_words = request.split("\n")
        method = split_words[0].split()[0]
        size = split_words[0].split()[1].replace("/", "")
        print(split_words[0])

        if method == 'GET' and size.isdigit():
            size = int(size)
            if 100 <= size <= 20000:
                filename = "/index.html"
                create_html(size)
                file_input = open("." + filename)
                content = file_input.read()
                file_input.close()
                response = ""
                response += str('HTTP/1.0 200 OK\r\n')
                response += str('Content-Length: ' + str(len(content)) + '\r\n')
                response += str('Content-Type: text/html; charset=UTF-8' + '\r\n\r\n')
                print(response)
                client.sendall(response.encode())
                response = content
                response_bytes = response.encode()
                client.sendall(response_bytes)
            else:
                filename = "400.html"
                file_input = open(filename)
                content = file_input.read()
                file_input.close()
                response = ""
                response += str('HTTP/1.0 400 Bad Request\r\n')
                response += str('Content-Length: ' + str(len(content)) + '\r\n')
                response += str('Content-Type: text/html; charset=UTF-8' + '\r\n\r\n')
                print(response)
                client.sendall(response.encode())
                response = content
                response_bytes = response.encode()
                client.sendall(response_bytes)
        else:
            if method in valid_methods:
                filename = "501.html"
                file_input = open(filename)
                content = file_input.read()
                file_input.close()
                response = ""
                response += str('HTTP/1.0 501 Not Implemented\r\n')
                response += str('Content-Length: ' + str(len(content)) + '\r\n')
                response += str('Content-Type: text/html; charset=UTF-8' + '\r\n\r\n')
                print(response)
                client.sendall(response.encode())
                response = content
                response_bytes = response.encode()
                client.sendall(response_bytes)
            else:
                filename = "400.html"
                file_input = open(filename)
                content = file_input.read()
                file_input.close()
                response = ""
                response += str('HTTP/1.0 400 Bad Request\r\n')
                response += str('Content-Length: ' + str(len(content)) + '\r\n')
                response += str('Content-Type: text/html; charset=UTF-8' + '\r\n\r\n')
                print(response)
                client.sendall(response.encode())
                response = content
                response_bytes = response.encode()
                client.sendall(response_bytes)
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

print('Socket is listening..')

server_socket.listen(5)  # TODO: what is ?

while True:
    client, address = server_socket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (client,))
    numOfThread += 1
    print('Thread Number: ' + str(numOfThread))
server_socket.close()
