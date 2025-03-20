#import socket module
from socket import *
from datetime import datetime
import sys
import os

server_socket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
server_socket.bind(('localhost', 12001))
server_socket.listen(1)
while True:
    #Establish the connection
    print('Ready to serve...')
    connection_socket, addr = server_socket.accept()
    try:
        message = connection_socket.recv(2048).decode()
        filename = message.split()[1]
        print("open file: " + filename[1:])
        f = open(filename[1:])
        outputdata = []
        #Send one HTTP header line into socket
        outputdata.append("HTTP/1.1 200 OK")
        outputdata.append("Connection: close")
        outputdata.append("Date: " + datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"))
        outputdata.append("Last-Modified: " + datetime.fromtimestamp(os.fstat(f.fileno()).st_mtime).strftime("%a, %d %b %Y %H:%M:%S %Z"))
        outputdata.append("Content-Length: " + str(os.fstat(f.fileno()).st_size + 2))
        outputdata.append("Content-Type: text/html")
        for i in range(0, len(outputdata)):
            connection_socket.send(outputdata[i].encode())
            connection_socket.send("\r\n".encode())
        #Send the content of the requested file to the client
        connection_socket.send("\r\n".encode()) # entity body preceded by a CRLF
        connection_socket.send(f.read().encode())
        connection_socket.close()
    except IndexError:
        print(message + "IndexError")
        continue
    except IOError:
        f = open("WebPage404.html")
        outputdata = []
        #Send response message for file not found
        outputdata.append("HTTP/1.1 404 Not Found")
        outputdata.append("Connection: close")
        outputdata.append("Date: " + datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"))
        outputdata.append("Last-Modified: " + datetime.fromtimestamp(os.fstat(f.fileno()).st_mtime).strftime("%a, %d %b %Y %H:%M:%S %Z"))
        outputdata.append("Content-Length: " + str(os.fstat(f.fileno()).st_size + 2))
        outputdata.append("Content-Type: text/html")
        for i in range(0, len(outputdata)):
            connection_socket.send(outputdata[i].encode())
            connection_socket.send("\r\n".encode())
        #Close client socket
        connection_socket.send("\r\n".encode()) #entity body preceded by a CRLF
        connection_socket.send(f.read().encode())
        connection_socket.close()
server_socket.close()
sys.exit()#Terminate the program after sending the corresponding data
