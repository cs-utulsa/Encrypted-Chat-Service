import socket
import sys
import string
import random

ip = 'localhost'
port = 120 #specified port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates a tcp socket.


try:
  sock.connect(('127.0.0.1', 8888)) #accept the connection from the client
  #print("client connected using ", sock[0],":",sock[1])#address:port
  data = " ".join(random.choice(string.ascii_uppercase + string.digits)
              for i in range(20))
  sock.sendall(bytes(data, "utf-8")) #sends string to client to communicate with server
  received = str(sock.recv(1024), "utf-8") #the string the server actually recieved 
  
  print("Sent:     {}".format(data))
  print("Received: {}".format(received))
except socket.timeout:
  print("timeout")