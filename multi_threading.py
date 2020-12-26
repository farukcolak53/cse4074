import socket
from _thread import *
from sys import argv
import codecs

valid_methods = ['POST', 'UPDATE', 'DELETE', 'HEAD', 'PUT', 'PATCH']


def write_message(size):
    str = "a"
    for i in range(size - 50):
        str = str + "a"
    return str


def create_html(filename, size):
    file = open(filename, 'w')

    message = """<HTML>
<HEAD>
<TITLE>I am """ + str(size) + """ bytes long</TITLE>
</HEAD>
<BODY>""" + str(write_message(size)) + """</BODY>
</HTML>"""

    file.write(message)
    file.close()


def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    response = ""
    while True:

        request = connection.recv(2048)
        request = request.decode('utf-8')
        split_words = str(request).split()
        method = split_words[0]
        size = split_words[1].replace("/", "")

        if method == 'GET' and size.isdigit():
            size = int(size)
            if 100 <= size <= 20000:
                filename = str(size) + ".html"
                create_html(filename, size)
                file_input = open(filename)
                content = file_input.read()
                file_input.close()

                response = ""
                response += str('HTTP/1.0 200 OK\r\n')
                response += str('Content-Length: ' + str(size) + '\r\n')
                response += str('Content-Type: text/html; charset=UTF-8' + '\r\n\r\n')
                response += "http://localhost:8080/" + filename

        else:
            if method in valid_methods:
                response = str('HTTP/1.0 501 Not Implemented \r\n')
            else:
                response = str('HTTP/1.0 400 Bad Request \r\n')
        if not request:
            break
        client.sendall(response.encode())
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
