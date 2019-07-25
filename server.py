import socket
import os

OPTIONS = "server_config"
file = open(OPTIONS, "r")
lines = file.read().split("\n")
HOST = lines[0].split(":")[1]
PORT = int(lines[1].split(":")[1])
PATH = lines[2].split(":")[1]
file.close()
os.chdir(PATH)

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(2)
print("Listening for connections")
conn, addr = sock.accept()
print("{} is connected".format(addr))

msg = conn.recv(1024)
info = str(msg).split("'")[1].split(" ")
file_name = info[1]
buffer = int(info[2])
print(file_name)
conn.send(bytes("confirm: sending {} {}".format(file_name, buffer).encode()))
msg = conn.recv(1024)
if msg == b'confirm':
	conn.send(b'confirm')
	file = open(file_name, "wb+")
	while True:
		data = conn.recv(buffer)
		if not data:
			break
		file.write(data)
print("The file has been recieved")
