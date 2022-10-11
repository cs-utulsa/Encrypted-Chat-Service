from asyncio.windows_events import NULL
import socket

class ChatServer:
    def __init__(self, port_number):
        ################################################
        # Parameters
        ################################################
        self.port_number = port_number

        ################################################
        # Variables
        ################################################
        self.DEFAULT_IP = "localhost"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP Socket Var
        self.server.settimeout(30) # sets time socket will wait for a connection; 30s
    
    # NULL parms
    # binds the socket from constructor to given port number; returns connection and address
    # Throws err if incorrect IP:Port is given, or timesout; returns null
    def connect(self):
        try:
            self.server.bind((self.DEFAULT_IP, self.port_number)) # locks server socket to IP:PORT
            self.server.listen(1) # waits for connection
            return self.server.accept()
        except:
            print("ERR: no connection made")
            return NULL

    # Returns the socket's portnumber
    def get_port(self):
        return self.server.getsockname() 
        
    # Sets port number given in constructor to new port number
    def set_port(self, port_num): 
        self.port_number = port_num

if __name__ == "__main__":
    PORT = 20

    ## Constructor and connect Test
    server = ChatServer(PORT)
    conn, addr = server.connect()

    ## receiving data from made connection & send back in uppercase
    data = conn.recv(1024).strip()
    print("{} wrote: ".format(addr))
    print(data)
    conn.sendall(data.upper())

    ## get_port Test
    print("server on port: {}".format(server.get_port()))