import socket


class TCPServer(object):
    def run(self):
        # Create String with Server Name
        servername = "THREEONEOH-T470 SERVER"
        # Accept Connection
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(('0.0.0.0', 6789))
        # OSError: [Errno 99] Cannot assign requested address
        serversocket.listen(5) # queue up as many as 5 connect requests before refusing outside connections
        print('starts listen')
        while True:
            # Receive client message:
            (clientsocket, address) = serversocket.accept()
            clientmsg = clientsocket.recv(4096)
            # Print the client's name from the message and the server's name
            try:
                arr = clientmsg.decode().split(":")
                clientname = arr[0]
                clientint = int(arr[1])
                if 1 <= clientint <= 100:
                    pass
                else:
                    raise ValueError("Integer not between 1 to 100")
                    # If server receives an integer value that is out of range, terminate after releasing any created sockets, and shutdown the server.
                    clientsocket.shutdown(socket.SHUT_RDWR)
                    clientsocket.close()
                    serversocket.shutdown(socket.SHUT_RDWR)
                    serversocket.close()
            except ValueError as ex:
                print("Error on split %s: %s" % (clientmsg, ex))
            print("client name: %s server name: %s" % (clientname, servername))
            serverint = 99
            # Pick an integer between 1 and 100 and write to screen output: client's number, server's number, sum of those numbers
            print("client int: %s server int: %s sum: %s" % (clientint, serverint, clientint + serverint))
            # Send server's name and chosen integer back to the client.
            strmsg = servername + ":" + str(serverint)
            clientsocket.send(strmsg.encode())


if __name__ == '__main__':
    TCPServer().run()
