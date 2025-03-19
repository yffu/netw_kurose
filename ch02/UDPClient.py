import socket
# https://docs.python.org/3/library/socket.html


class UDPClient(object):
    def run(self):
        try:
            client_int = int(input("Enter integer from 1 to 100: "))
        except ValueError as ex:
            print("Error on converting %s: %s" % (client_int, ex))
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_name = "T470 Client"
        msg = client_name + ":" + str(client_int)
        client_socket.sendto(msg.encode(), ('localhost', 12000))
        server_msg, server_ip = client_socket.recvfrom(1024)
        try:
            server_msg = server_msg.decode()
            arr = server_msg.split(":")
            server_name = arr[0]
            server_int = int(arr[1])
            if server_int != 0:
                print("client name: %s server name: %s" % (client_name, server_name))
                print("client int: %s server int: %s sum: %s" % (client_int, server_int, client_int + server_int))
        except Exception as ex:
            print("Err: %s; ServerMsg: %s" % (ex, server_msg.decode()))
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()


if __name__ == '__main__':
    UDPClient().run()
