import socket
from _thread import *
import sys
import functions


# "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --proxy-bypass-list="<-loopback>"


def proxy_thread(connection):
    request = connection.recv(9999)
    if not request:
        return
    request = request.decode('utf-8')
    request_split = request.split("\n")

    if ":" in request_split[0]:
        method = request_split[0].split()[0]
        if method != 'GET':
            return
        print("----------------------------")
        print("---------Request------------")
        print(request)
        print("----------------------------")
        server_port = request_split[0].split("/")[2].split(":")[1]
        size = request_split[0].split("/")[3].split()[0]
        url = "/" + size
        request_split[0] = method + " " + url + " HTTP/1.1"
    else:
        method = request_split[0].split()[0]
        server_port = "8080"
        size = request_split[0].split()[1][1:]
        url = "/" + size
        request_split[0] = method + " " + url + " HTTP/1.1"
    # print(method, server_port, size, url)

    try:
        # create a socket to connect to the web server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", int(server_port)))

        if int(size) > 9999:
            filename = "414.html"
            functions.generate_response_html(filename, connection)
            return
        request = ("\r\n".join(request_split) + "\r\n\r\n").encode()
        s.send(request)  # send request to web server
        # print(request)
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
        functions.generate_response_html(filename, connection)
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

print('Proxy socket is listening..')

proxy_socket.listen(10)

while True:
    client, address = proxy_socket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(proxy_thread, (client,))
    proxy_thread_num += 1
    print('Proxy Thread Number: ' + str(proxy_thread_num))
proxy_socket.close()
