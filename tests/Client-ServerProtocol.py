import socket
import sys

#client-server protocol for testing purposes

HOST, PORT = "localhost", 20
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
  try: 
  # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))
  except socket.error as error:
	  print("Failed to connect. The error specifies %s" %(error)) #specifies errors
	  sys.exit() #force exit when error occurs.

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")
  
print("The connection to the server was established using: " + address[0]+ ":"
	+ str(address[1])))
print("String sent: ".format(string))
print("String recieved: ".format(received))