import socket
import select
from message import Message

class EChatClient():
    """
    Constructor for Encrypted Chat Client server.

    :param host: Host's IP addr/hostname to use for socket
    :param port: Host's IP port number for socket
    """
    HOST = ""
    PORT = 0
    outputs = []
    message_queue = []
    client_socket = None

    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
    
    def connect(self):
        """
        Tries to connect and bind socket to provided HOST and PORT address given in constructor. Will loop six times
        trying to form a connection if an error occurs.

        :return: true if a connection is made; otherwise false
        """
        count = 1
        while(count < 6):
            try:
                myClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
                myClient.connect((self.HOST, self.PORT))
                myClient.setblocking(0)
                self.client_socket = myClient
                return True
            except:
                count=count+1
                continue
        return False
    
    def sendMsg(self, message: Message):
        """
        Sends the message given as a parameter through `client_socket`.

        :param message: full message constructed from `message.py` class
        """
        self.client_socket.sendall(message.getData().encode('utf8'))

    def readAvailable(self):
        """
        If there is an available socket in the list `read_sockets`, read the message in and return the message.

        :return: if there is a message, returns message; otherwise returns None
        """
        try:
            read_sockets, write_sockets, error_sockets = select.select([self.client_socket], [], [], 0)
            for sock in read_sockets:
                msg = Message()
                msg.parseMsg(sock.recv(1024).decode('utf8'))
                return msg
        except:
            return None

    def close(self):
        """
        Gracefully closes `client_socket` and ends program.
        """
        self.client_socket.close()

    def getPort(self):
        """
        Returns PORT field of `client_socket`

        :return: int PORT
        """
        return self.PORT

    def setPort(self, port):
        """
        Sets PORT

        :param port: int port to set `client_socket` to
        """
        self.PORT = port

    def getIP(self):
        """
        Returns IP address/hostname of `client_socket`

        :return: address/hostname of `client_socket`
        """
        return self.HOST

    def setIP(self, IP):
        """
        Sets a new IP address/hostname of `client_socket`

        :param IP: address/hostname of `client_socket`
        """
        self.HOST = IP