import socket
class client():
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as guest:
            guest.connect((self.HOST, self.PORT))
            if(guest.connected):
                return "Connected"
            else:
                return "null"
        
    def getPort(self):
        return self.PORT

    def setPort(self, port):
        self.PORT = port

    def getIP(self):
        return self.HOST

    def setIP(self, IP):
        self.HOST = IP

    def main():
        print("hello")
