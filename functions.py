# Functions class

from sys import getsizeof


def write_message(size):
    text = "a"
    for i in range(size - 84):
        text = text + "a"
    return text


def create_requested_document(size):
    index_file = open("./index.html", 'w+')
    body_text = str(write_message(size))
    content = "<html>\n<head>\n"
    content += "<title> I am " + str(size) + " bytes</title>\n</head>\n<body>\n<p>"
    content += body_text
    content += "</p>\n</body>\n</html>"
    index_file.write(content)
    return index_file


def generate_response_html(filename, connection):
    response = ""
    if filename == '/index.html':
        file_input = open("." + filename)
        content = file_input.read()
        response += str('HTTP/1.0 200 OK\r\n')
    elif filename == '400.html':
        file_input = open(filename)
        content = file_input.read()
        response += str('HTTP/1.0 400 Bad Request\r\n')
    elif filename == '501.html':
        file_input = open(filename)
        content = file_input.read()
        response += str('HTTP/1.0 501 Not Implemented\r\n')
    elif filename == '414.html':
        file_input = open(filename)
        content = file_input.read()
        response += str('HTTP/1.0 414 Request-URI Too Long\r\n')
    elif filename == '404.html':
        file_input = open(filename)
        content = file_input.read()
        response += str('HTTP/1.0 404 Not Found\r\n')

    file_input.close()
    response += str('Content-Length: ' + str(len(content)) + '\r\n')
    response += str('Content-Type: text/html; charset=UTF-8' + '\r\n\r\n')
    print("----------------------------")
    print("---------Response-----------")
    print(response)
    print("----------------------------")
    connection.sendall(response.encode())
    response = content
    response_bytes = response.encode()
    connection.sendall(response_bytes)