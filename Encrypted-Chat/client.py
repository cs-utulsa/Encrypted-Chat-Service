import socket
class client():
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
    
    def connect(self):
        count = 1
        myClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        myClient.connect((self.HOST, self.PORT))
        if(myClient.connect == True):
            return myClient
        elif(myClient.connect == False and count < 6):
            count = count + 1
            self.connect()
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
    print("kaljsdf;lkj")
    today = client("127.232.232.11", 1232)
    if (today.connect == True):
        print("We are connected")
    else:
        print("We are")

main()