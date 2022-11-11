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

    def connect(self):
        """
        Binds the socket from constructor to given port number, waits for a connection, then adds socket to an array to
        prevent blocking.

        :return: None if err occurs
        """
        try:
            self.server.bind((self.DEFAULT_IP, self.port_number)) # locks server socket to IP:PORT
            self.server.listen(1) # waits for connection
            self.sockets.append(self.server)
        except:
            print("ERR: no connection made")
            return None

    def get_port(self):
        """
        Gets the server's port number

        :return: int port_number
        """
        return self.server.getsockname() 

    def set_port(self, port_num):
        """
        Sets server port number to the new port number

        :param port_num: new port number
        :return: None
        """
        self.port_number = port_num

    def sendMsg(self, message: Message):
        """
        Sends a string to ...

        :param message: ASCII string to send
        :return:
        """
        for socket in self.sockets:
            if socket != self.server:
                socket.sendall(message.getData().encode('utf8'))

    def readAvailable(self):
        """
        Reads messages from sockets ...

        :return: String msg received
        """
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
        """
        Closes all sockets in self.sockets array
        :return: None
        """
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