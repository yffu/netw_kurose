import socket


class TCPServer(object):
    def run(self):
        server_name = "T470 SERVER"
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 12001))
        server_socket.listen(1)
        while True:
            connection_socket, address = server_socket.accept()
            client_msg = connection_socket.recv(1024).decode()
            try:
                arr = client_msg.split(":")
                client_name = arr[0]
                client_int = int(arr[1])
                if 1 <= client_int <= 100:
                    server_int = 99
                else:
                    server_int = 0
                    server_msg = server_name + ":" + str(server_int)
                    connection_socket.send(server_msg.encode())
                    break
            except ValueError as ex:
                print("Error on split %s: %s" % (client_msg, ex))
            print("client name: %s server name: %s" % (client_name, server_name))
            print("client int: %s server int: %s sum: %s" % (client_int, server_int, client_int + server_int))
            server_msg = server_name + ":" + str(server_int)
            connection_socket.send(server_msg.encode())
            connection_socket.shutdown(socket.SHUT_RDWR)
            connection_socket.close()
        server_socket.close()


if __name__ == '__main__':
    TCPServer().run()
