import socket
import select
from crypto.encrypt import ECEncrypt
from net.message import Message
from crypto.handshake import RSAHandshake
import time
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
        try:
            for msg in message.getData():
                # This is because windows sockets are dumb and dont seperate packets if they arrive too fast
                # time.sleep(0.0001)
                data = self.encrypt_pair.encrypt(msg.encode('utf8'))
                print("CLI_SND_LEN: ", len(data))
                self.client_socket.sendall(data)
        except:
            return

    def readAvailable(self):
        try:
            read_sockets, write_sockets, error_sockets = select.select([self.client_socket], [], [], 0)
            for sock in read_sockets:
                msg = Message()
                total_content = ""
                #try:
                while True:
                    tmp_msg = Message()
                    #pkt_len = int.from_bytes(sock.recv(2), "big")
                    #print("CLI_RCV_LEN: ",pkt_len)
                    #if pkt_len > 4096:
                    #    print("Client read overflow")
                    #    print(sock.recv(2048))
                    #    exit()
                    edata = sock.recv(10000000)
                    print("RAW: ", edata)
                    data = self.encrypt_pair.decrypt(edata)
                    #print(f'DECRYPT: {data}')
                    tmp_msg.parseMsg(data)
                    total_content += tmp_msg.getContent()
                    if tmp_msg.getHeader('seg').split(':')[0] == tmp_msg.getHeader('seg').split(':')[1]:
                        msg.setHeaders(tmp_msg.getHeaders())
                        print("Done Fragmenting")
                        break
                #except Exception as e:
                #   print("ReadAvailable ", e)
                #   return None
                msg.setContent(total_content)
                return msg
        except Exception as e:
            print(e)
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