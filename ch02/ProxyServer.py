from socket import *
import sys
import os

# http://127.0.0.1:12001/gaia.cs.umass.edu/kurose_ross/eighth.php try as a simple html page
class ProxyServer(object):
    def run(self):
        if len(sys.argv) <= 1:
            print('Usage : "python ProxyServer.py server_ip"\n[server_ip] : It is the IP Address Of Proxy Server')
            sys.exit(2)
        # Create a server socket, bind it to a port and start listening
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((sys.argv[1], 12001))
        server_socket.listen(1)
        while True:
            # Start receiving data from the client
            print('Ready to serve...')
            connection_socket, addr = server_socket.accept()
            print('Received a connection from:', addr)
            message = connection_socket.recv(1024).decode()
            print(message)
            # Extract the filename from the given message
            print(message.split()[1])
            file_name = message.split()[1].partition("/")[2]
            file_to_use = '/' + file_name
            file_exists = False
            print("file_name: %s\t file_to_use: %s" % (file_name, file_to_use))
            try:
                # Check whether the file exist in the cache
                f = open(file_to_use[1:], "r")
                output_data = f.readlines()
                file_exists = True
                # ProxyServer finds a cache hit and generates a response message
                connection_socket.send("HTTP/1.0 200 OK\r\n".encode())
                connection_socket.send("Content-Type:text/html\r\n".encode())
                connection_socket.send("\r\n".encode())
                for l in output_data:
                    connection_socket.send(l.encode())
                    connection_socket.send("\r\n".encode())
                connection_socket.send("\r\n.\r\n".encode())
                f.close()
                print('Read from cache')
            # Error handling for file not found in cache
            except IOError:
                if not file_exists:
                    # Create a socket on the proxy server
                    client_socket = socket(AF_INET, SOCK_STREAM)
                    host_name = file_name.split('/')[0].replace("www.", "", 1)
                    print("host_name: %s" % host_name)
                try:
                    # Connect to the socket to port 80
                    client_socket.connect((host_name, 80))
                    # Create a temporary file on this socket and ask port 80 for the file requested by the client
                    send_cmd = "GET " + '/' + file_name.partition('/')[2] + " HTTP/1.0\r\n\r\n"
                    print(send_cmd)
                    client_socket.send(send_cmd.encode('utf-8'))
                    # Read the response into buffer
                    f_s = client_socket.makefile('r', None)
                    # Create a new file in the cache for the requested file.
                    # Also send the response in the buffer to client socket and the corresponding file in the cache
                    os.makedirs(os.path.dirname(file_name), exist_ok=True)
                    with open(file_name, "w+") as f:
                        for line in f_s:
                            print(line)
                            f.write(line)
                except Exception as Ex:
                    print(str(Ex))
                else:
                    # HTTP response message for file not found
                    f = open("WebPage404.html")
                    output_data = list()
                    output_data.append("HTTP/1.1 404 Not Found")
                    output_data.append("Connection: close")
                    output_data.append("Content-Type: text/html")
                    for i in range(0, len(output_data)):
                        connection_socket.send(output_data[i].encode())
                        connection_socket.send("\r\n".encode())
                    connection_socket.send("\r\n".encode())     # Entity body preceded by a CRLF
                    connection_socket.send(f.read().encode())
                    # Close the client and the server sockets
                    client_socket.shutdown(socket.SHUT_RDWR)
                    client_socket.close()
                    connection_socket.shutdown(socket.SHUT_RDWR)
                    connection_socket.close()
        server_socket.shutdown(socket.SHUT_RDWR)
        server_socket.close()


if __name__ == '__main__':
    ProxyServer().run()
