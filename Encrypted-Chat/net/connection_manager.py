import threading
from net.hclient import EChatClient
from net.hserver import EChatServer
from net.message import Message
import datetime

class ConnectionManager():
    """
    This is the intermidiary class for handling connections between users for both host and client
    """
    USERNAME = "NULL_USER"
    IS_CONNECTED = False
    IS_HOST = False
    SERVER = None 
    CLIENT = None

    # Sets the username
    def setUsername(self, username:str):
        self.USERNAME = username

    def isConnected(self) -> bool:
        """Returns True if the connection manager still has an open socket

        Returns:
            bool: Connection State
        """
        return self.IS_CONNECTED

    def createRoom(self, target:str="0.0.0.0", port:int=8888):
        """Create a new room for chatting. This is the function the HOST calls to start a room

        Args:
            target (str, optional): Defaults to "0.0.0.0".
            port (int, optional): Defaults to 8888.
        """
        self.IS_HOST = True
        self.SERVER = EChatServer(target, port)
        self.SERVER.connect()
        self.IS_CONNECTED = True

    def connectToRoom(self, target:str="127.0.0.1", port:str=8888):
        """Connect to a room at TARGET:PORT. This is the function a client calls to connect to a host

        Args:
            target (str, optional): Defaults to "127.0.0.1".
            port (str, optional): Defaults to 8888.
        """
        self.IS_HOST = False
        self.CLIENT = EChatClient(target, port)
        self.CLIENT.connect()
        self.IS_CONNECTED = True
    
    def sendMessage(self, msg:Message):
        """This function sends a message object to the client/s or server that you are connected to

        Args:
            msg (Message): Message to send
        """
        if self.IS_HOST:
            self.SERVER.sendMsg(msg)
        else:
            self.CLIENT.sendMsg(msg)

    def getNextMessage(self) -> Message:
        """Returns the next message received. MUST BE CALLED AFTER connectToRoom OR createRoom HAS BEEN ESTABLISHED. This function is blocking!

        Returns:
            Message: The message object received
        """
        if self.IS_HOST:
            return self.SERVER.readAvailable()
        else:
            return self.CLIENT.readAvailable()

    def close(self):
        """Calls all the necessary functions to close connections to the server/client
        """
        if self.IS_CONNECTED:
            try:
                msg = Message()
                msg.setHeader("message_type", "control")
                msg.setHeader("username", self.USERNAME)
                if self.IS_HOST and self.SERVER != None:
                    msg.setContent("SERVER CLOSE")
                    self.sendMessage(msg)
                    self.SERVER.close()
                elif self.CLIENT != None:
                    msg.setContent("CLOSING")
                    self.sendMessage(msg)
                    self.CLIENT.close()
            except Exception as e:
                print("Socket could not be closed: ", e)
        self.IS_CONNECTED = False
        self.IS_HOST = False
        self.CLIENT = None
        self.SERVER = None