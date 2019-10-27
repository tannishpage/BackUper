import socket
import os
import sys

SERVERIP = "2001:8003:e041:9b00:dd13:4822:8fc0:1497"
PORT = 5000

def send_data(master, file, ip, port, buffer=1024):
	sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
	sock.connect((SERVERIP, PORT, 0, 0))
	file.seek(0, 2)
	size = file.tell()
	file.seek(0, 0)
	message = "sending {} {}".format(master+".zip", buffer)
	sock.send(bytes(message.encode()))
	if sock.recv(1024) == bytes("confirm: {}".format(message).encode()):
		sock.send(b"confirm")
		if sock.recv(1024) == b"confirm":
			sent_size = 0
			while True:
				data = file.read(buffer)
				sent_size = len(data) + sent_size
				sys.stdout.write("\rProgress: {:.3f}%".format(100*(sent_size/size)))
				sock.send(data)
				if not data:
					break
	return True

def main():
	file_name = sys.argv[1]
	print(file_name)
	try:
		send_data(file_name, open(file_name, "rb"), SERVERIP, PORT, 8192)
		print("File has been send")
	except Exception as e:
		print(e)
		print("File might not have been sent, try again")

main()
