import socket
import select
from message import Message

class EChatServer:
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
        self.sockets = []
    # NULL parms
    # binds the socket from constructor to given port number; returns connection and address
    # Throws err if incorrect IP:Port is given, or timesout; returns null
    def connect(self):
        try:
            self.server.bind((self.DEFAULT_IP, self.port_number)) # locks server socket to IP:PORT
            self.server.listen(1) # waits for connection
            self.sockets.append(self.server)
        except:
            print("ERR: no connection made")
            return None

    # Returns the socket's portnumber
    def get_port(self):
        return self.server.getsockname() 
        
    # Sets port number given in constructor to new port number
    def set_port(self, port_num): 
        self.port_number = port_num

    def sendMsg(self, message: Message):
        for socket in self.sockets:
            if socket != self.server:
                socket.sendall(message.getData().encode('utf8'))

    def readAvailable(self):
        read_sockets, write_sockets, error_sockets = select.select(self.sockets, [], [], 0)
        for socket in read_sockets:
            if socket == self.server:
                print("Connected to client")
                self.sockets.append(self.server.accept()[0])
            else:
                try:
                    msg = Message()
                    msg.parseMsg(socket.recv(1024).decode('utf8'))
                    return msg
                except:
                    print("Client Disconnected")
                    self.sockets.remove(socket)
                    socket.close()
        return None
        
    def close(self):
        for sock in self.sockets:
            sock.close()
            
if __name__ == "__main__":
    PORT = 20

    ## Constructor and connect Test
    server = EChatServer(PORT)
    conn, addr = server.connect()

    ## receiving data from made connection & send back in uppercase
    data = conn.recv(1024).strip()
    print("{} wrote: ".format(addr))
    print(data)
    conn.sendall(data.upper())

    ## get_port Test
    print("server on port: {}".format(server.get_port()))