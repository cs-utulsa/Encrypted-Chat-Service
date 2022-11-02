import socket
import select
from encrypt import ECEncrypt
from message import Message
from rsahandshake import RSAHandshake

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
        """

        :return:
        """
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
        """

        :param message:
        :return:
        """
        self.client_socket.sendall(self.encrypt_pair.encrypt(message.getData().encode('utf8')))

    def readAvailable(self):
        """

        :return:
        """
        read_sockets, write_sockets, error_sockets = select.select([self.client_socket], [], [], 0)
        for sock in read_sockets:
            msg = Message()
            msg.parseMsg(sock.recv(1024).decode('utf8'))
            return msg
        return None

    def close(self):
        """

        :return:
        """
        self.client_socket.close()

    def getPort(self):
        """

        :return:
        """
        return self.PORT

    def setPort(self, port):
        """

        :param port:
        :return:
        """
        self.PORT = port

    def getIP(self):
        """

        :return:
        """
        return self.HOST

    def setIP(self, IP):
        """

        :param IP:
        :return:
        """
        self.HOST = IP
if __name__ == "__main__":
    PORT = 120

    ## Constructor and connect Test
    client = EChatClient(PORT)
    conn, addr = client.connect()

    ## receiving data from made connection & send back in uppercase
    data = conn.recv(1024).strip()
    print("{} wrote: ".format(addr))
    print(data)
    conn.sendall(data.upper())

    ## get_port Test
    print("server on port: {}".format(server.get_port())) 
