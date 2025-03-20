import socket
import datetime
import time


class UDPPingerClient(object):
    def run(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(1)
        for i in range(10):
            client_msg = "Ping:\t %i\t %s" % (i + 1, datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"))
            try:
                time_st = time.monotonic_ns()
                # (1) send the ping message using UDP (Note: Unlike TCP, you do not need to establish a connection
                # first, since UDP is a connectionless protocol.)
                # time.sleep(1)
                client_socket.sendto(client_msg.encode(), ('localhost', 12000))
                server_msg, server_ip = client_socket.recvfrom(1024)
                time_end = time.monotonic_ns()
                # (2) print the response message from server, if any
                print(server_msg.decode())
                # (3) calculate and print the round trip time (RTT), in seconds, of each packet, if server responses
                print("RRT:\t %i \t %i ns" % (i + 1, time_end - time_st))
            except socket.timeout as ex:
                # (4) otherwise, print “Request timed out”
                print("Ping:\t %i\t %s" % (i + 1, ex))
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()


if __name__ == '__main__':
    UDPPingerClient().run()


