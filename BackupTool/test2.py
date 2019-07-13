import socket
def send_data(file, ip, port):
    s = socket.socket()
    s.connect((ip, port))
    sending = True
    s.send(b"can_send_bro?")
    if s.recv(1024) == b"yea_bro":
        s.send(b"im_sending_bro")
        if s.recv(1024) == b"ready_bro":
            while sending:
                data = file.read(8192)
                s.send(data)
                if not data:
                    break
