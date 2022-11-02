import threading
from client import EChatClient
from ChatServer import EChatServer
from message import Message
import datetime
from App import App
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


class Chat():
    """
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
                print(f'[{d}] {self._username}> {input_message}')
                msg = Message(input_message)
                msg.setHeader('username', self._username)
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
                print(f'[{d}] {self._username}> {input_message}')
                msg = Message(input_message)
                msg.setHeader('username', self._username)
                server.sendMsg(msg)
            recv = server.readAvailable()
            if recv != None:
                d = datetime.datetime.now()
                print(f'[{d}] {recv.getHeader("username")}> {recv.getContent()}')
        server.close()
        self._input_thread.join()
        return True
