import os
import sys
import zipfile
import socket
import datetime
import time
import getpass

OPTIONS = "options"
BKPLIST_START = 7
IP = 0
SENDFILE = 1
DEVICE = 5
KEEP = 2
AUTOBACKUP = 3
AUTOBACKUPFREQ = 4

def zipp(foldername, target_dir):
	zipobj = zipfile.ZipFile(foldername + '.zip', 'w', zipfile.ZIP_DEFLATED)
	rootlen = len(target_dir) + 1
	for base, dirs, files in os.walk(target_dir):
		for count, file in enumerate(files):
			fn = os.path.join(base, file)
			zipobj.write(fn, fn[rootlen:])
			print("Added: {}".format(fn))
	else:
		return True

def create_backup(master, backup_list):
	for zip_dir in backup_list:
		sys.stdout.write("\rZipping {}...\n".format(zip_dir))
		zipp(zip_dir.split("/")[-1], zip_dir)
	os.chdir("..")
	sys.stdout.write("Zipping master...\n")
	zipp(master, master)
	sys.stdout.write("Zipping master...Done\n")
	path = os.getcwd() + "/{}.zip".format(master)
	return path


def send_data(master, file, ip, port, buffer=1024):
	s = socket.socket()
	s.connect((ip, port))
	message = "sending {} {}".format(master+".zip", buffer)
	s.send(bytes(message.encode()))
	if s.recv(1024) == bytes("confirm: {}".format(message).encode()):
		s.send(b"confirm")
		if s.recv(1024) == b"confirm":
		  while True:
		    data = file.read(buffer)
		    s.send(data)
		    if not data:
        		break
	return True

def get_backup_list():
	file = open(OPTIONS, 'r')
	backup_list = file.read().split("\n")[BKPLIST_START:-1]
	return backup_list

def get_server_addr():
	file = open(OPTIONS, 'r')
	ip_port = file.read().split("\n")[IP].split(":")
	return ip_port[1], int(ip_port[2])

def get_send_file():
	file = open(OPTIONS, 'r')
	send_file = file.read().split("\n")[SENDFILE].split(":")[1]
	if send_file.lower() == "yes":
		return True
	else:
		return False

def get_device():
	file = open(OPTIONS, 'r')
	device_name = file.read().split("\n")[DEVICE].split(":")[1]
	return device_name

def keep_backup_after_send():
	file = open(OPTIONS, 'r')
	keep = file.read().split("\n")[KEEP].split(":")[1]
	if keep.lower() == "yes":
		return True
	else:
		return False

def auto_backup():
	file = open(OPTIONS, 'r')
	auto = file.read().split("\n")[AUTOBACKUP].split(":")[1]
	if auto.lower() == "yes":
		return True
	else:
		return False

def auto_backup_freq():
	file = open(OPTIONS, 'r')
	freq = file.read().split("\n")[AUTOBACKUPFREQ].split(":")[1]
	return freq

def clean(master):
	try:
		os.chdir(master)
		for x in os.listdir(os.getcwd()):
			os.remove(x)
		os.chdir("..")
		os.rmdir(master)
	except PermissionError:
		print("Couldn't remove the master folder. Please delete it manually or run this program as sudo next time")

def main():
	backup_list = get_backup_list()
	ip, port = get_server_addr()
	send_file = get_send_file()
	keep = keep_backup_after_send()
	date = "".join(str(datetime.datetime.date(datetime.datetime.now())).split("-"))
	time = "".join(str(datetime.datetime.now()).split(" ")[1].split(".")[0].split(":"))
	device = get_device()
	if sys.platform == "linux" or sys.platform == "linux2":
		os.chdir("/home/{}".format(getpass.getuser()))
	elif sys.platform == "darwin":
		os.chdir("/Users/{}".format(getpass.getuser()))
	elif sys.platform == "win32":
		pass
	master = "backup_{}_{}_{}".format(date, time, device)
	os.mkdir(master)
	os.chdir(master)
	path = create_backup(master, backup_list)
	if send_file:
		print("Finished making backup, sending file to {}", ip)
		send_data(master, open(path, 'rb'), ip, port)
		print("Backup file sent successfully")
		if not keep:
			os.remove(master+".zip")
	else:
		print("\nBackup has been created. It is located at {}\n".format(path))
	clean(master)

if __name__ == "__main__":
	auto = auto_backup()
	if auto:
		freq = int(auto_backup_freq())
		try:
			while True:
				main()
				time.sleep(freq)
		except KeyboardInterrupt:
			print("Quitting")
			exit()
	else:
		main()
