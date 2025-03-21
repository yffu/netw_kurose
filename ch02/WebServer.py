from socket import *
from datetime import datetime
import sys
import os


class WebServer(object):
    def run(self):
        server_socket = socket(AF_INET, SOCK_STREAM)
        # Prepare a sever socket
        server_socket.bind(('localhost', 12001))
        server_socket.listen(1)
        while True:
            # Establish the connection
            print('Ready to serve...')
            connection_socket, addr = server_socket.accept()
            try:
                message = connection_socket.recv(2048).decode()
                filename = message.split()[1]
                print("open file: " + filename[1:])
                f = open(filename[1:])
                output_data = list()
                # Send one HTTP header line into socket
                output_data.append("HTTP/1.1 200 OK")
                output_data.append("Connection: close")
                output_data.append("Date: " + datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"))
                output_data.append("Last-Modified: " + datetime.fromtimestamp(os.fstat(f.fileno()).st_mtime).strftime("%a, %d %b %Y %H:%M:%S %Z"))
                output_data.append("Content-Length: " + str(os.fstat(f.fileno()).st_size + 2))
                output_data.append("Content-Type: text/html")
                for i in range(0, len(output_data)):
                    connection_socket.send(output_data[i].encode())
                    connection_socket.send("\r\n".encode())
                # Send the content of the requested file to the client
                connection_socket.send("\r\n".encode())     # Entity body preceded by a CRLF
                connection_socket.send(f.read().encode())
                connection_socket.close()
            except IndexError as Ex:
                print("IndexError: " + str(Ex))
                continue
            except IOError:
                f = open("WebPage404.html")
                output_data = list()
                # Send response message for file not found
                output_data.append("HTTP/1.1 404 Not Found")
                output_data.append("Connection: close")
                output_data.append("Date: " + datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"))
                output_data.append("Last-Modified: " + datetime.fromtimestamp(os.fstat(f.fileno()).st_mtime).strftime("%a, %d %b %Y %H:%M:%S %Z"))
                output_data.append("Content-Length: " + str(os.fstat(f.fileno()).st_size + 2))
                output_data.append("Content-Type: text/html")
                for i in range(0, len(output_data)):
                    connection_socket.send(output_data[i].encode())
                    connection_socket.send("\r\n".encode())
                # Close client socket
                connection_socket.send("\r\n".encode())     # Entity body preceded by a CRLF
                connection_socket.send(f.read().encode())
                connection_socket.close()
        server_socket.close()
        sys.exit()      # Terminate the program after sending the corresponding data


if __name__ == '__main__':
    WebServer().run()
