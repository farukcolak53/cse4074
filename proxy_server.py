import socket
from _thread import *
import sys


def proxy_thread(connection):
    request = connection.recv(9999)
    if not request:
        return
    request = request.decode('utf-8')
    # http://localhost:8888//localhost:8080/500
    request_split = request.split("\n")
    print(request)

    if ":" in request_split[0]:
        method = request_split[0].split()[0]
        server_port = request_split[0].split("/")[2].split(":")[1]
        size = request_split[0].split("/")[3].split()[0]
        url = request_split[0].split()[1]
        url = url[2:]
        url1 = "/" + size
        request_split[0] = method + " " + url1 + " HTTP/1.1"
    else:
        method = request_split[0].split()[0]
        server_port = "8080"
        size = request_split[0].split()[1][1:]
        url = "/" + size
        url1 = "/" + size
        request_split[0] = method + " " + url1 + " HTTP/1.1"
    print(method, server_port, size, url, url1)

    try:
        # create a socket to connect to the web server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", int(server_port)))

        if int(size) > 9999:
            filename = "414.html"
            file_input = open(filename)
            content = file_input.read()
            file_input.close()
            response = ""
            response += str('HTTP/1.0 414 Request-URI Too Long\r\n')
            response += str('Content-Length: ' + str(len(content)) + '\r\n')
            response += str('Content-Type: text/html; charset=UTF-8' + '\r\n\r\n')
            print(response)
            connection.sendall(response.encode())
            response = content
            response_bytes = response.encode()
            connection.sendall(response_bytes)
            connection.close()
            return
        request = ("\r\n".join(request_split) + "\r\n\r\n").encode()
        s.send(request)  # send request to webserver
        print(request)
        while True:
            # receive data from web server
            data = s.recv(9999)
            if not data:
                break
            connection.send(data)
        s.close()
        connection.close()
    except socket.error as e:
        if s:
            s.close()
        filename = "404.html"
        file_input = open(filename)
        content = file_input.read()
        file_input.close()
        response = ""
        response += str('HTTP/1.0 404 Not Found\r\n')
        response += str('Content-Length: ' + str(len(content)) + '\r\n')
        response += str('Content-Type: text/html; charset=UTF-8' + '\r\n\r\n')
        print(response)
        connection.sendall(response.encode())
        response = content
        response_bytes = response.encode()
        connection.sendall(response_bytes)
        connection.close()
        return


proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
# port = int(argv[1])
port = 8888

proxy_thread_num = 0

try:
    proxy_socket.bind((host, port))
except socket.error as e:
    if proxy_socket:
        proxy_socket.close()
    print(str(e))

print('Socket is listening..')

proxy_socket.listen(10)  # TODO: what is ?

while True:
    client, address = proxy_socket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(proxy_thread, (client,))
    proxy_thread_num += 1
    print('Proxy Thread Number: ' + str(proxy_thread_num))
proxy_socket.close()
