import os
import sys
import zipfile
import socket
import datetime
import getpass

OPTIONS = "options"
BKPLIST_START = 8
IP = 0
SENDFILE = 1
DEVICE = 6

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
		sys.stdout.write("\rZipping {}...".format(zip_dir))
		zipp(zip_dir.split("/")[-1], zip_dir)
		sys.stdout.write("Zipping {}...Done".format(zip_dir))
	os.chdir("..")
	sys.stdout.write("Zipping master...")
	zipp(master, master)
	sys.stdout.write("Zipping master...Done")
	path = os.getcwd() + "{}.zip".format(master)
	return path


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

def get_backup_list():
	file = open(OPTIONS, 'r')
	backup_list = file.read().split("\n")[BKPLIST_START:-1]
	return backup_list


def get_server_addr():
	file = open(OPTIONS, 'r')
	ip = file.read().split("\n")[IP].split(":")[1]
	return ip

def get_send_file():
	file = open(OPTIONS, 'r')
	send_file = file.read().split("\n")[SENDFILE].split(":")[1]
	if send_file == "yes":
		return True
	else:
		return False

def get_device():
	file = open(OPTION, 'r')
	device_name = file.read().split("\n")[DEVICE].split(":")[1]
	return device_name

def initialize():
	if sys.platform == "linux" or sys.platform == "linux2":
		os.chdir("/home/{}".format(getpass.getuser()))
	elif sys.platform == "darwin":
		os.chdir("/Users/{}".format(getpass.getuser()))
	elif sys.platform == "win32":
		pass
	backup_list = get_backup_list()
	server_addr = get_server_addr()
	send_file = get_send_file()
	date = str(datetime.datetime.date(datetime.datetime.now()))
	device = get_device()
	master = "{}-{}".format(date, device)
	os.mkdir(master)
	os.chdir(master)
	path = create_back(master, backup_list)
	send_data(open(path, 'r'), ip, 5000)	
"""
class Options:
	def __init__(self):
		self._options = self.load_options()
		self._backup_list = get_backup_list()

	def load_options(self):
		options_file = open(OPTIONS, 'r')
		all_options = {}
		for count, op in enumerate(options_file.read().split("\n")):
			s = op.split(":")
			if count == 6:
				break
			all_options[s[0]] = s[1]

	def list_options(self):
		

	def options(self):
		self.list_options()
		while True:
			input("> ")
"""
