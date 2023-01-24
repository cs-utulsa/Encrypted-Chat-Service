#!python3.10

#Basic imports
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox
import os
import datetime
import threading
import textwrap
from PIL import Image, ImageTk

#Hermes imports
from ChatServer import EChatServer
from client import EChatClient
from message import Message

#Working directory stuff that we'll need in the future for the installer
NATIVEDIR = os.path.dirname(os.path.abspath(__file__))
ASSETDIR = os.path.join(NATIVEDIR, "assets")

#App graphics constants
APPNAME = "Hermes"
X_PADDING = 15
Y_PADDING = 10
FONT = ("OCRB", 12)
PRIMARY_COLOR = '#57B400'

#Random Constants
SERVER = 0
CLIENT = 1

class message_widget(tk.Frame):
    def __init__(self, parent, prof, username, msg, datetime):
        tk.Frame.__init__(self, parent)
        self.image = Image.open(prof).resize((50,50))
        self.prof = ImageTk.PhotoImage(self.image)
        self.label = ttk.Label(self, image=self.prof)
        self.label.grid(row=0, column=0, rowspan=2)

        self.user_text = ttk.Label(self, text=username, font=("OCRB", 12, 'bold'))
        self.user_text.grid(row=0, column=1, sticky="sw", padx=(10,0))

        self.grid_columnconfigure(2, weight=1)
        self.time_text = ttk.Label(self, text=f'[{datetime}'[:-10]+"]", font=("OCR", 10))
        self.time_text.grid(row=0, column=2, sticky="sw", padx=(5,0))

        self.msg_text = ttk.Label(self, text=msg, font=FONT, wraplength=800)
        self.msg_text.grid(row=1, column=1, rowspan=2, columnspan=2, sticky="nw", padx=(10,0), pady=(0,15))

#The entire App class
class App(tk.Tk):

    def __init__(self, username="Developer"):
        super().__init__()

        self.username = username

        self.style = ttk.Style("cyborg")
        self.style.configure('TButton', background=PRIMARY_COLOR, bordercolor=PRIMARY_COLOR, lightcolor=PRIMARY_COLOR, darkcolor=PRIMARY_COLOR)
        self.style.map('TButton', background=[('disabled',PRIMARY_COLOR), ('active',PRIMARY_COLOR)])
        self.style.map('TButton', lightcolor=[('disabled',PRIMARY_COLOR), ('active',PRIMARY_COLOR)])
        self.style.map('TButton', bordercolor=[('disabled',PRIMARY_COLOR), ('active',PRIMARY_COLOR)])
        self.style.map('TButton', darkcolor=[('disabled',PRIMARY_COLOR), ('active',PRIMARY_COLOR)])

        #Defining some app information
        self.title(APPNAME)
        self.geometry('960x540')
        self.resizable(False, False)
        self.iconbitmap(ASSETDIR+'\\icon.ico')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.running = True

        #Class variables relating to server stuff
        self.connection = None
        self.target = None
        self.port = None
        self.messages = []

        #Creates the GUI
        self.bindings()
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
        # self.msg_list.insert(tk.END, "CONNECTED TO "+self.target+":"+str(self.port)) #This adds a connected message to the texts
        thread = threading.Thread(target=self.listen)
        thread.start()

    def listen(self):
        #This is run by a separate thread that is always looking for incoming messages and posts them to the texts
        while self.running:
            recv = self.connection.readAvailable()
            if recv != None:
                msg = recv.getContent()
                d = datetime.datetime.now()
                message_widget(self.scrollable_frame, 'prof.png', self.username, msg, d).pack(anchor=tk.W)
                # self.msg_list.insert(tk.END, f'[{d}] {recv.getHeader("username")}> {msg}')
        self.connection.close()

    def send(self, event=None):
        #Sends a message and adds it to the texts list
        msg = self.entry_field.get()
        if msg == "":
            return
        ecmsg = Message(msg)
        ecmsg.setHeader('username', self.username)
        # self.connection.sendMsg(ecmsg) #TESTING BY DAWSON
        self.entry_field.delete(0, tk.END)
        d = datetime.datetime.now()
        message_widget(self.scrollable_frame, 'prof.png', self.username, msg, d).pack(anchor=tk.W)

    def bindings(self):
        self.bind('<Return>', self.send)

    def create_widgets(self):
        #Settings frame is where the IP and port options are
        settings_frame = tk.Frame(highlightbackground="gray", highlightthickness=2)
        settings_frame.pack(side=tk.TOP, fill=tk.X, padx=X_PADDING, pady=Y_PADDING)
        image = Image.open(ASSETDIR+'\\full_logo.png')
        img = image.resize((int(1920/16), int(1080/16)))
        self.my_img = ImageTk.PhotoImage(img)
        label = ttk.Label(settings_frame, image=self.my_img)
        label.pack(side=tk.LEFT, padx=(0,100))
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

        #Texts frame is where all the texts are displayed
        texts_frame = ttk.Frame()
        texts_frame.pack(fill=tk.BOTH, expand=True, padx=15)
        canvas = tk.Canvas(texts_frame)
        scrollbar = ttk.Scrollbar(texts_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        #Send frame is where you enter and send texts
        send_frame = ttk.Frame()
        my_msg = tk.StringVar()
        self.entry_field = ttk.Entry(send_frame, textvariable=my_msg, font=FONT)
        self.entry_field.pack(padx=(0,X_PADDING), side=tk.LEFT, fill=tk.X, expand=tk.TRUE)
        send_button = ttk.Button(send_frame, text="Send", command=lambda: self.send())
        send_button.pack(side=tk.RIGHT)
        send_frame.pack(padx=X_PADDING, pady=Y_PADDING, fill=tk.X)

if __name__ == "__main__":
    app = App()
    app.mainloop()
