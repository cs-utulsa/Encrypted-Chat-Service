import threading
#from Client import EChatClient
#from Server import EChatServer
from message import Message

class InputHandler():
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


class Cli():
    """
    The Cli class is used for parsing the command arguments and handling
    user input to be passed to the host or client objects.
    """
    _args = None
    _input_thread = None


    def __init__(self, args: list):
        self._args = args
        self._user_input = InputHandler()

    def readInput(self, input_handler: InputHandler):
        usr_inp = ''
        while usr_inp != '!exit' or self._user_input.run != True:
            usr_inp = input('Input> ')
            input_handler.setMessage(usr_inp)
        self._user_input.run = False

    def client_mode(self):
        target = self._args.target[0]
        port = self._args.port[0]

        self._input_thread = threading.Thread(target=self.readInput, args=(self._user_input,))
        self._input_thread.start()
        #client = EChatClient()
        print(self._args)
        #client.connect(target, port)
        input_message = ''
        while self._user_input.run:
            input_message = self._user_input.getMessage()
            if input_message is not None:
                #client.sendMsg(Message(input_message))
                print(input_message)
            #recv_msg = client.readMsg()
            #if recv_msg is not None:
            #    print(recv_msg.getContent())
        self._input_thread.join()
        return True


    def server_mode(self):
        target = self._args.local_ip[0]
        port = self._args.port[0]
        #client = EChatClient()
        print(self._args)
        #server.bind(target, port)
        
        input_message = ''
        while self._user_input.run:
            input_message = self._user_input.getMessage()
            if input_message is not None:
                #client.sendMsg(Message(input_message))
                print(input_message)
            #recv_msg = client.readMsg()
            #if recv_msg is not None:
            #    print(recv_msg.getContent())
        self._input_thread.join()
        return True
