import threading
from net.hclient import EChatClient
from net.hserver import EChatServer
from net.message import Message
import datetime
from gui.app import App

class InputHandler():
    """
    Do not modify this class it is used to poll user input 
    because python does not have functionality to do that.
    """
    def __init__(self):
        self.lock = threading.Lock()
        self.value = None
        self.run = True

    def setMessage(self, value):
        self.lock.acquire()
        try:
            self.value = value
        finally:
            self.lock.release()

    def killHandler(self):
        self.lock.acquire()
        try:
            self.run = False
        finally:
            self.lock.release()

    def getMessage(self):
        self.lock.acquire()
        try:
            return self.value
        finally:
            self.value = None
            self.lock.release()
            
class fInput():
    """
    The fInput class is used for reading in and placing files. 
    When a user sends a file, they will use a button on the GUI to start the process. 
    Tkinter will aid in selecting the path of the file. 
  
    The fInput class will read in the file and save it as a string.
    Then return the file object. 
    
    """
    def __init__(self):
        self.filename = None

    def fReadFile(self, path):
        try:
            with open(path, "rb") as file:
                self.filename = os.path.basename(path)
                return file.read()
        except:
            return None

    def getFileName(self):
        return self.filename

    def fCreateFile(self, file, path):
        try:
            with open(path + self.filename, "wb") as new_file:
                new_file.write(file)
            return True
        except:
            return False

class Chat():
    """
    WARNING - LEGACY CLI CHAT CLASS
    
    The Chat class is used for parsing the command arguments and handling
    user input to be passed to the host or client objects.
    """
    _args = None
    _input_thread = None
    username = "TEST_USR"

    def __init__(self, args: list, username:str):
        self._args = args
        self._user_input = InputHandler()
        self.username = username

    def readInput(self, input_handler: InputHandler):
        usr_inp = ''
        while usr_inp != '!exit' or self._user_input.run != True:
            usr_inp = input('')
            input_handler.setMessage(usr_inp)
        self._user_input.run = False

    def client_mode(self):
        """
        This function implements the client functionality of the program. 
        A new thread is started to handle local user input.
        The client will then reach out to the server and establish a connection
        before sending and receiving data.
        """
        target = self._args.ip[0]
        port = self._args.port[0]

        self._input_thread = threading.Thread(target=self.readInput, args=(self._user_input,))
        self._input_thread.start()

        client = EChatClient(target, port)
        client.setIP(target)
        client.setPort(port)
        if not client.connect():
            return False

        input_message = ''

        while self._user_input.run:
            input_message = self._user_input.getMessage()
            if input_message is not None:
                d = datetime.datetime.now()
                print ("\033[A                             \033[A")
                print(f'[{d}] {self.username}> {input_message}')
                msg = Message(input_message)
                msg.setHeader('username', self.username)
                client.sendMsg(msg)
            recv = client.readAvailable()
            if recv != None:
                d = datetime.datetime.now()
                print(f'[{d}] {recv.getHeader("username")}> {recv.getContent()}')
        self._input_thread.join()
        client.close()
        return True


    def server_mode(self):
        target = self._args.ip[0]
        port = self._args.port[0]

        self._input_thread = threading.Thread(target=self.readInput, args=(self._user_input,))
        self._input_thread.start()

        server = EChatServer(port, ip_address=target)
        server.connect()
        input_message = ''
        msg = Message(input_message)
        print(f'[+] Successfully bound to {target}:{port}')
        print('[+] Listening for clients...')
        while self._user_input.run:
            input_message = self._user_input.getMessage()
            if input_message is not None:
                d = datetime.datetime.now()
                print ("\033[A                             \033[A")
                print(f'[{d}] {self.username}> {input_message}')
                msg = Message(input_message)
                msg.setHeader('username', self.username)
                server.sendMsg(msg)
            recv = server.readAvailable()
            if recv != None:
                d = datetime.datetime.now()
                print(f'[{d}] {recv.getHeader("username")}> {recv.getContent()}')
        server.close()
        self._input_thread.join()
        return True
