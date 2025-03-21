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
        send_cmd = 'HELO Client\r\n'
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
        ssl_sock.send('EHLO client\r\n'.encode())
        data = ssl_sock.recv(1024)
        print(data.decode())
        username = 'test_user'
        password = 'test_pwd'
        send_msg = 'AUTH LOGIN\r\n'
        ssl_sock.send(send_msg.encode())
        data = ssl_sock.recv(1024).decode()
        print(data[4:])
        data = base64.b64decode(data[4:]).decode('utf-8')
        print(data)
        send_msg = base64.b64encode(username.encode('utf-8')).decode('utf-8') + '\r\n'
        print(send_msg)
        ssl_sock.send(send_msg.encode())
        data = ssl_sock.recv(1024).decode()
        print(data)
        data = base64.b64decode(data[4:]).decode('utf-8')
        print(data)
        send_msg = base64.b64encode(password.encode('utf-8')).decode('utf-8') + '\r\n'
        print(send_msg)
        ssl_sock.send(send_msg.encode())
        data = ssl_sock.recv(1024).decode()
        print(data)
        # https://www.samlogic.net/articles/smtp-commands-reference-auth.htm
        # this works but you need 2 factor authentication as of 2025 > the following status code is returned even after correct username and password provided
        # 534-5.7.9 Application-specific password required. For more information, go to
        # 534 5.7.9  https://support.google.com/mail/?p=InvalidSecondFactor d2e1a72fcca58-73906159dd5sm929236b3a.135 - gsmtp


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
