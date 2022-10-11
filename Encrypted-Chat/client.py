import socket
class client():
    HOST = ""
    PORT = 0
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
    
    def connect(self):
        count = 1
        while(count < 6):
            try:
                myClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
                myClient.connect((self.HOST, self.PORT))
                return myClient
                break
            except:
                count=count+1
                continue
        return "null"
        
    def getPort(self):
        return self.PORT

    def setPort(self, port):
        self.PORT = port

    def getIP(self):
        return self.HOST

    def setIP(self, IP):
        self.HOST = IP