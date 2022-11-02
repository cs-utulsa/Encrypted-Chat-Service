import socket
import sys

#Server side tester for ChatServer.py

ip = ''
port = 120 #specified port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates a tcp socket.
string = " ".join(sys.argv[1:])

try:
	sock.bind((ip, port)) #Binds the defaults host and specified port.
	sock.listen(5) #listen to first 6 open ports. The max is ussualy 5. This applies when not on a local port
  
  print (server started)
except socket.error as error:
	print("Failed to connect. The error specifies %s" %(error)) #specifies errors
	sys.exit() #force exit when socket is created.


while True:
  client, address = sock.accept() #accept the connection from the client
  print("client connected using ", address[0],":",address[1])#address:port
  
  client.sendall(bytes(data + "\n", "utf-8")) #sends string to client to communicate with server
  received = str(sock.recv(1024), "utf-8") #the string the server actually recieved
  
  print("String sent: ".format(string))
  print("String recieved: ".format(received))