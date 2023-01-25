import socket
import select
from crypto.encrypt import ECEncrypt
from net.message import Message
from crypto.handshake import RSAHandshake

class EChatClient():
    HOST = ""
    PORT = 0
    outputs = []
    message_queue = []
    client_socket = None
    encrypt_pair = None
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
    
    def connect(self):
        count = 1
        while(count < 6):
            try:
                myClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
                myClient.connect((self.HOST, self.PORT))
                self.client_socket = myClient
                hs = RSAHandshake()
                ekey, dkey = hs.handshake(myClient)
                self.encrypt_pair = ECEncrypt(ekey, dkey)
                return True
            except Exception as e:
                print(e)
                count=count+1
                continue
        return False
    
    def sendMsg(self, message: Message):
        self.client_socket.sendall(self.encrypt_pair.encrypt(message.getData().encode('utf8')))

    def readAvailable(self):
        read_sockets, write_sockets, error_sockets = select.select([self.client_socket], [], [], 0)
        for sock in read_sockets:
            msg = Message()
            edata = sock.recv(1024)
            try:
                data = self.encrypt_pair.decrypt(edata)
                print(f'DECRYPT: {data}')
                msg.parseMsg(data)
            except Exception as e:
                print(e)
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