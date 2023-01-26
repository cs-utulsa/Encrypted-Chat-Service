import socket
import select
import rsa
from crypto.encrypt import ECEncrypt
from net.message import Message
from crypto.handshake import RSAHandshake
import time
class EChatServer:
    def __init__(self, ip_address="0.0.0.0", port_number=8888):
        self.port_number = port_number
        self.IP_ADDRESS = ip_address
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        
        # Sets the time socket will wait for a connection; 30s
        self.server.settimeout(30)
        self.sockets = []
        self.crypt_pair = {}

    def connect(self):
        """
        Binds the socket from constructor to given port number, waits for a connection, then adds socket to an array to
        prevent blocking.

        :return: None if err occurs
        """
        try:
            # locks server socket to IP:PORT
            self.server.bind((self.IP_ADDRESS, self.port_number))
            # waits for connection
            self.server.listen(1)
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

    def sendMsg(self, message: Message, exclusion=None):
        """
        Sends a string to ...

        :param message: ASCII string to send
        :return:
        """
        for socket in self.sockets:
            if socket != self.server and socket != exclusion:
                em = self.crypt_pair[socket]
                for msg in message.getData():
                    print(msg)
                    print(len(msg))
                    # This is because windows sockets are dumb and dont seperate packets if they arrive too fast
                    time.sleep(0.0001)
                    socket.sendall(em.encrypt(msg.encode('utf8')))

    def readAvailable(self):
        """
        Reads messages from sockets ...

        :return: String msg received
        """
        read_sockets, write_sockets, error_sockets = select.select(self.sockets, [], [], 0)
        for socket in read_sockets:
            if socket == self.server:
                print("Connected to client")
                csock = self.server.accept()[0]
                self.sockets.append(csock)
                hs = RSAHandshake()
                ekey, dkey = hs.handshake(csock=csock, srv=True)
                enc = ECEncrypt(ekey,dkey)
                self.crypt_pair[csock] = enc
            else:
                try:
                    msg = Message()
                    em = self.crypt_pair[socket]
                    total_content = ""
                    while True:
                        tmp_msg = Message()
                        data = em.decrypt(socket.recv(2048))
                        print(f'DECRYPT: {data}')
                        tmp_msg.parseMsg(data)
                        total_content += tmp_msg.getContent()
                        
                        # Check if client is disconnecting
                        if msg.getHeader("message_type") == "control" and msg.getContent() == "CLOSING":
                            del self.crypt_pair[socket]
                            socket.close()
                            del socket
                        if tmp_msg.getHeader('seg').split(':')[0] == tmp_msg.getHeader('seg').split(':')[1]:
                            msg.setHeaders(tmp_msg.getHeaders())
                            print("Done Fragmenting")
                            break
                    msg.setContent(total_content)
                    self.sendMsg(msg, exclusion=socket)
                    return msg
                except Exception as e:
                    print(e)
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