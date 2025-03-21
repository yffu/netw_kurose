import socket
import ssl
import base64

class SMTPClient(object):
    def run1(self):
        server_name = 'smtp.gmail.com'
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_name, 587))
        recv = client_socket.recv(1024).decode()
        print(recv)
        if recv[:3] != '220':
            print('220 reply not received from server.')
        send_cmd = 'HELO tester\r\n'
        client_socket.send(send_cmd.encode())
        recv = client_socket.recv(1024).decode()
        print(recv)
        if recv[:3] != '250':
            print('250 reply not received from server.')
        # Send MAIL FROM command and print server response.
        # send_cmd = 'MAIL FROM: <test_send@gmail.com>\r\n'
        client_socket.send('STARTTLS\r\n'.encode())
        recv = client_socket.recv(1024).decode()
        print(recv)
        ssl_sock = context.wrap_socket(client_socket, server_hostname=server_name)
        ssl_sock.send('EHLO tester\r\n'.encode())
        data = ssl_sock.recv(1024)
        print(data.decode())
        ssl_sock.send('AUTH LOGIN\r\n'.encode())
        data = ssl_sock.recv(1024)
        print(data.decode())
        # https://tedboy.github.io/python_stdlib/generated/generated/smtplib.SMTP.starttls.html
        # but how to implement using send/recv on the ssl socket?


    def run(self):
        end_msg = "\r\n.\r\n"
        # Choose a mail server (e.g. Google mail server) and call it mailserver
        # Create socket called clientSocket and establish a TCP connection with mailserver
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('smtp.freesmtpservers.com', 25))
        # client_socket.connect(('smtp.gmail.com', 587))
        recv = client_socket.recv(1024).decode()
        if recv[:3] != '220':
            print('220 reply not received from server.')
        # Send HELO command and print server response.
        send_cmd = 'HELO tester\r\n'
        client_socket.send(send_cmd.encode())
        recv = client_socket.recv(1024).decode()
        print(recv)
        if recv[:3] != '250':
            print('250 reply not received from server.')
        # Send MAIL FROM command and print server response.
        send_cmd = 'MAIL FROM: <test_send@gmail.com>\r\n'
        client_socket.send(send_cmd.encode())
        recv = client_socket.recv(1024).decode()
        print(recv)
        if recv[:3] != '250':
            print('250 reply not received from server.')
        # Send RCPT TO command and print server response.
        send_cmd = 'RCPT TO: <test_recv@gmail.com>\r\n'
        client_socket.send(send_cmd.encode())
        recv = client_socket.recv(1024).decode()
        print(recv)
        if recv[:3] != '250':
            print('250 reply not received from server.')
        # Send DATA command and print server response.
        send_cmd = 'DATA\r\n'
        client_socket.send(send_cmd.encode())
        recv = client_socket.recv(1024).decode()
        print(recv)
        if recv[:3] != '354':
            print('354 reply not received from server.')
        # Send message data.
        send_msg = ["Subject: You Like?\n\n", "\r\nDo you like ketchup!", "\r\nHow about pickles?", end_msg]
        for m in send_msg:
            client_socket.send(m.encode())
        # Message ends with a single period.
        recv = client_socket.recv(1024).decode()
        print(recv)
        if recv[:3] != '250':
            print('250 reply not received from server.')
        # Send QUIT command and get server response.
        send_cmd = 'QUIT\r\n'
        client_socket.send(send_cmd.encode())
        recv = client_socket.recv(1024).decode()
        print(recv)
        if recv[:3] != '221':
            print('221 reply not received from server.')

        # go here to check for email https://www.wpoven.com/tools/free-smtp-server-for-testing


if __name__ == '__main__':
    SMTPClient().run()
    # SMTPClient().run1()
