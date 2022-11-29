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

#ECS imports
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

class TextBubble:
    def __init__(self,master,is_sender,message=""):
        self.master = master
        self.is_sender = is_sender
        self.frame = tk.Frame(master)
        time_label = tk.Label(self.frame,text=datetime.datetime.now().strftime("%d-%m-%Y %X"))
        message_label = tk.Label(self.frame, text=textwrap.fill(message, 25))
        if is_sender:
            self.frame.configure(bg=PRIMARY_COLOR)
            message_label.configure(bg=PRIMARY_COLOR, font=FONT)
            time_label.configure(bg=PRIMARY_COLOR, font=FONT)
        else:
            self.frame.configure(bg="gray")
            message_label.configure(bg="gray", font=FONT)
            time_label.configure(bg="gray", font=FONT)
        time_label.grid(row=0,column=0,sticky="w",padx=5)
        message_label.grid(row=1, column=0,sticky="w",padx=5,pady=3)
        if is_sender:
            self.i = self.master.create_window(960-250,340,window=self.frame,anchor='w')
            self.master.create_polygon(self.draw_triangle_sender(self.i), fill=PRIMARY_COLOR, outline=PRIMARY_COLOR)
        else:
            self.i = self.master.create_window(70,340,window=self.frame,anchor='w')
            self.master.create_polygon(self.draw_triangle_receiver(self.i), fill="gray", outline="gray")

    def draw_triangle_sender(self,widget):
        x1, y1, x2, y2 = self.master.bbox(widget)
        return x1 + 180, y2 - 10, x1 + 195, y2 + 10, x1 + 180, y2
    
    def draw_triangle_receiver(self,widget):
        x1, y1, x2, y2 = self.master.bbox(widget)
        return x1, y2 - 10, x1 - 15, y2 + 10, x1, y2

#The entire App class
class App(tk.Tk):

    def __init__(self, username):
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
                self.msg_list.insert(tk.END, f'[{d}] {recv.getHeader("username")}> {msg}')
            if self.messages:
                self.canvas.move(tk.ALL, 0, -80)
            a = TextBubble(self.canvas,False,message=msg)
            self.messages.append(a)
        self.connection.close()

    def send(self, event=None):
        #Sends a message and adds it to the texts list
        msg = self.entry_field.get()
        if msg == "":
            return
        ecmsg = Message(msg)
        ecmsg.setHeader('username', self.username)
        self.connection.sendMsg(ecmsg)
        self.entry_field.delete(0, tk.END)
        if self.messages:
            self.canvas.move(tk.ALL, 0, -80)
        a = TextBubble(self.canvas,True,message=msg)
        self.messages.append(a)

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
        texts_frame.pack(padx=X_PADDING, fill=tk.BOTH, expand=tk.TRUE)
        self.canvas = tk.Canvas(texts_frame)
        self.canvas.pack(fill=tk.BOTH, expand=tk.TRUE)

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
