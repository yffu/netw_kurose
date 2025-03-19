import socket
# https://pythontic.com/modules/socket/udp-client-server-example


class UDPServer(object):
    def run(self):
        server_name = "T470 Server"
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('localhost', 12000))
        while True:
            client_msg, client_ip = server_socket.recvfrom(1024)
            try:
                arr = client_msg.decode().split(":")
                client_name = arr[0]
                client_int = int(arr[1])
                if 1 <= client_int <= 100:
                    server_int = 89
                else:
                    server_int = 0
                    server_msg = server_name + ":" + str(server_int)
                    server_socket.sendto(server_msg.encode(), client_ip)
                    break
                print("client name: %s server name: %s" % (client_name, server_name))
                print("client int: %s server int: %s sum: %s" % (client_int, server_int, client_int + server_int))
                server_msg = server_name + ":" + str(server_int)
                server_socket.sendto(server_msg.encode(), client_ip)
            except ValueError as ex:
                print("Error on split %s: %s" % (client_msg, ex))
        server_socket.shutdown(socket.SHUT_RDWR)
        server_socket.close()


if __name__ == '__main__':
    UDPServer().run()
