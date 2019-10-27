import sys
import time
file =  open("LICENSE", 'rb')
size = file.seek(0, 2)
print(size)
file.seek(0, 0)
buffer =  1
sent = 0
while True:
	data = file.read(buffer)
	sent += len(data)
	percent = sent/size * 100
	sys.stdout.write("\rProgress: [{}{}] {:.1f}%".format("="*int(percent/10), "."*(10 - int(percent/10)), percent))
	sys.stdout.flush()
	time.sleep(0.001)
	if not data:
		break
