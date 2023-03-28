import socket


class TCPClient(object):
    def run(self):
        # Input Stream from keyboard
        # Accept integer from 1 to 100
        try:
            clientint = int(input("Enter any integer from 1 to 100: "))
        except ValueError as ex:
            print("Error on converting %s: %s" % (clientint, ex))
        # Open TCP socket to your server
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(("192.168.0.145", 6789))
        clientname = "THREEONEOH-T470 CLIENT"
        # Send Client Name + Integer
        bytemsg = clientname + ":" + str(clientint)
        clientsocket.send(bytemsg.encode())
        # Wait for a server reply
        servermsg = clientsocket.recv(4096)
        try:
            arr = servermsg.decode().split(":")
            print(arr)
            servername = arr[0]
            serverint = int(arr[1])
        except ValueError as ex:
            print("Error on split %s: %s" % (servermsg, ex))
        print("client name: %s server name: %s" % (clientname, servername))
        print("client int: %s server int: %s sum: %s" % (clientint, serverint, clientint + serverint))
        # Terminate after releasing any created sockets.
        clientsocket.shutdown(socket.SHUT_RDWR)
        # shutdown with option 3 is SHUT_RDWR, further sends and receives are disallowed.
        clientsocket.close()


if __name__ == '__main__':
    TCPClient().run()
