import socket
import ssl

class SMTPClient(object):
    def run(self):
        end_msg = "\r\n.\r\n"
        # Choose a mail server (e.g. Google mail server) and call it mailserver
        mail_server = 'smtp.freesmtpservers.com'
        # Create socket called clientSocket and establish a TCP connection with mailserver
        context = ssl.create_default_context()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((mail_server, 25))
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
