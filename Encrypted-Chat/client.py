import socket
import select
from message import Message

class EChatClient():
    HOST = ""
    PORT = 0
    outputs = []
    message_queue = []
    client_socket = None

    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
    
    def connect(self):
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
        self.client_socket.sendall(message.getData().encode('utf8'))

    def readAvailable(self):
        read_sockets, write_sockets, error_sockets = select.select([self.client_socket], [], [], 0)
        for sock in read_sockets:
            msg = Message()
            msg.parseMsg(sock.recv(1024).decode('utf8'))
            return msg
        return None

    def close(self):
        self.client_socket.close()

    def getPort(self):
        return self.PORT

    def setPort(self, port):
        self.PORT = port

    def getIP(self):
        return self.HOST

    def setIP(self, IP):
        self.HOST = IP