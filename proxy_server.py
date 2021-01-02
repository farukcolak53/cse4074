import os
import socket
from _thread import *
import functions


# "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --proxy-bypass-list="<-loopback>"


def proxy_thread(connection):
    request = connection.recv(9999)
    if not request:
        return
    request = request.decode('utf-8')
    request_split = request.split("\n")

    if "favicon.ico" in request_split[0]:
        return

    if "localhost" in request_split[0] or '127.0.0.1' in request_split[0]:
        method = request_split[0].split()[0]
        # if method != 'GET':
        #     return
        print("----------------------------")
        print("---------Request------------")
        print(request)
        print("----------------------------")
        hostname = "localhost"
        server_port = request_split[0].split("/")[2].split(":")[1]
        if server_port == '8080' or server_port == '8888':
            server_port = '8080'
        else:
            return
        size = request_split[0].split("/")[3].split()[0]
        url = "/" + size
        request_split[0] = method + " " + url + " HTTP/1.1"
    else:
        # any web server
        method = request_split[0].split()[0]
        hostname = request_split[0].split()[1].split(":")[0]
        server_port = request_split[0].split()[1].split(":")[1]
        size = "0"  # default

    try:
        # create a socket to connect to the web server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, int(server_port)))

        if int(size) > 9999:
            filename = "414.html"
            functions.generate_response_html(filename, connection)
            return
        request = ("\r\n".join(request_split) + "\r\n\r\n").encode()
        print(request.decode('utf-8'))

        my_path = "files" + request.decode('utf-8').split("\n")[0].split()[1]
        print("burada")
        print(my_path)
        with open('cache.txt') as f:
            if my_path in f.read():
                print("nerede")
                file_input = open(my_path)
                data = file_input.read()
                print(data)
                connection.sendall(data.encode())
                connection.close()
                return
        print("şurada")
        s.send(request)  # send request to web server
        while True:
            print("orada")
            # receive data from web server
            data = s.recv(9999)
            data_decoded_split = data.decode('utf-8').split("\n")
            if 'HTTP/1.0 200 OK' in data_decoded_split[0]:
                cache_file = open('cache.txt', 'a')
                filepath = "files/" + data_decoded_split[1].split()[1]
                cache_file.write(filepath + "\n")
                cache_file.close()
            if not data:
                break
            connection.send(data)
        s.close()
        connection.close()
    except socket.error as e:
        if s:
            s.close()
        filename = "404.html"
        print("patladı")
        functions.generate_response_html(filename, connection, 0)
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
