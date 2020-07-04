import subprocess
import time;

command = ['python', 'server.py']
while True:
	subprocess.call(command);
	time.sleep(1);
