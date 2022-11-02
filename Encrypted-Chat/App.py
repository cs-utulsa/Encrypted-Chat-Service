#!python3.10

#Basic imports
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox
import os
import datetime
import threading

#ECS imports
from ChatServer import EChatServer
from client import EChatClient
from message import Message

#Working directory stuff that we'll need in the future for the installer
NATIVEDIR = os.path.dirname(os.path.abspath(__file__))
ASSETDIR = os.path.join(NATIVEDIR, "assets")

#App graphics constants
APPNAME = "Encrypted Chat Service"
X_PADDING = 15
Y_PADDING = 10
FONT = ("Canva", 12)
PRIMARY_COLOR = '#57B400'

#Random Constants
SERVER = 0
CLIENT = 1

#The entire App class
class App(tk.Tk):

    def __init__(self):
        super().__init__()
        #Defining some app information
        self.title(APPNAME)
        # self.geometry('960x540')
        #pic = tk.PhotoImage(file=ASSETDIR+'\\icon.png')
        #self.iconphoto(False, pic)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.running = True

        #Class variables relating to server stuff
        self.connection = None
        self.target = None
        self.port = None

        #Creates the GUI
        self.create_widgets()

    def on_closing(self):
        #Kills the app when the 'x' is pressed
        self.running = False
        self.quit()
        self.destroy()

    def connect(self, target, port): #NOTE TO FUTURE SELF: RENAME THIS FUNCTION BECAUSE ITS USED IN SERVER CLASSES
        #Takes a target and port and determines whether you're client or server
        #This will be changed in this future. Just needed something quick for sprint 2
        self.target = target
        self.port = int(port)
        msg = "Would you like to open as server or client?"
        buttons = ["Server:primary", "Client"]
        mbox = Messagebox.show_question(msg, buttons=buttons, default="Server")
        if mbox == "Server":
            self.connection = EChatServer(self.port)
            self.start_connection()
        else:
            self.connection = EChatClient(self.target, self.port)
            self.start_connection()

    def start_connection(self):
        #Makes the connection and starts the "listening" thread
        self.connection.connect()
        self.msg_list.insert(tk.END, "CONNECTED TO "+self.target+":"+str(self.port)) #This adds a connected message to the texts
        thread = threading.Thread(target=self.listen)
        thread.start()

    def listen(self):
        #This is run by a separate thread that is always looking for incoming messages and posts them to the texts
        while self.running:
            recv = self.connection.readAvailable()
            if recv != None:
                msg = recv.getContent()
                d = datetime.datetime.now()
                self.msg_list.insert(tk.END, f'[{d}] NOT ME> {msg}')
        self.connection.close()

    def send(self, msg):
        #Sends a message and adds it to the texts list
        self.connection.sendMsg(Message(msg))
        self.entry_field.delete(0, tk.END)
        d = datetime.datetime.now()
        self.msg_list.insert(tk.END, f'[{d}] ME> {msg}')

    def create_widgets(self):
        #Settings frame is where the IP and port options are
        settings_frame = ttk.Frame()
        target = tk.StringVar()
        port = tk.StringVar()
        target_label = ttk.Label(settings_frame, text="Target IP:", font=FONT)
        target_label.pack(side=tk.LEFT, padx=(0,X_PADDING))
        target_entry = ttk.Entry(settings_frame, textvariable=target, font=FONT)
        target_entry.pack(side=tk.LEFT, padx=(0,X_PADDING))
        port_label = ttk.Label(settings_frame, text="Port:", font=FONT)
        port_label.pack(side=tk.LEFT, padx=(0,X_PADDING))
        port_entry = ttk.Entry(settings_frame, textvariable=port, font=FONT)
        port_entry.pack(side=tk.LEFT, padx=(0,X_PADDING))
        connect_button = ttk.Button(settings_frame, text="Connect", command=lambda: self.connect(target_entry.get(), port_entry.get()))
        connect_button.pack(side=tk.LEFT)
        settings_frame.pack(side=tk.TOP, padx=X_PADDING, pady=Y_PADDING)

        #Texts frame is where all the texts are displayed
        texts_frame = ttk.Frame()
        scrollbar = ttk.Scrollbar(texts_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list = tk.Listbox(texts_frame, yscrollcommand=scrollbar.set)
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        texts_frame.pack(padx=X_PADDING, fill=tk.BOTH, expand=tk.TRUE)

        #Send frame is where you enter and send texts
        send_frame = ttk.Frame()
        my_msg = tk.StringVar()
        self.entry_field = ttk.Entry(send_frame, textvariable=my_msg, font=FONT)
        self.entry_field.pack(padx=(0,X_PADDING), side=tk.LEFT, fill=tk.X, expand=tk.TRUE)
        send_button = ttk.Button(send_frame, text="Send", command=lambda: self.send(self.entry_field.get()))
        send_button.pack(side=tk.RIGHT)
        send_frame.pack(padx=X_PADDING, pady=Y_PADDING, fill=tk.X)

if __name__ == "__main__":
    app = App()
    app.mainloop()