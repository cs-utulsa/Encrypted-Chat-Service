#! python3

# Basic imports
import tkinter.filedialog
import tkinter as tk
from tkinter.font import Font
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox
import os
import datetime
import threading
import tempfile
import base64
from PIL import Image, ImageTk
import uuid
from ctypes import windll

# Hermes imports
from net.message import Message
from net.connection_manager import ConnectionManager

# Working directory stuff that we'll need in the future for the installer

# Gets this scripts current directory and then traverses up one
NATIVEDIR = os.path.dirname(os.path.abspath(__file__)) + "\\..\\"
ASSETDIR = os.path.join(NATIVEDIR, "assets")

#App graphics constants
APPNAME = "Hermes"
X_PADDING = 15
Y_PADDING = 10
FONT = ("OCRB", 12)
PRIMARY_COLOR = '#57B400'

#Custom Window constants
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
xwin = 0
ywin = 0

#Random Constants
SERVER = 0
CLIENT = 1

USER1 = "prof1.jpg"
USER2 = "prof2.jpg"

# Custom widget to show profile pic, username, time, and msg
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


# Custom widget to show image msg
class image_message_widget(tk.Frame):
    def __init__(self, parent, prof, username, img, datetime):
        tk.Frame.__init__(self, parent)
        try:
            print("IMAGE PATH:", img)
            self.img_res = Image.open(img).resize((500,500))
            self.tk_img = ImageTk.PhotoImage(self.img_res)
            self.image = Image.open(prof).resize((50,50))
            self.prof = ImageTk.PhotoImage(self.image)
            self.label = ttk.Label(self, image=self.prof)
            self.label.grid(row=0, column=0, rowspan=2)

            self.user_text = ttk.Label(self, text=username, font=("OCRB", 12, 'bold'))
            self.user_text.grid(row=0, column=1, sticky="sw", padx=(10,0))

            self.grid_columnconfigure(2, weight=1)
            self.time_text = ttk.Label(self, text=f'[{datetime}'[:-10]+"]", font=("OCR", 10))
            self.time_text.grid(row=0, column=2, sticky="sw", padx=(5,0))

            self.msg_text = ttk.Label(self, image=self.tk_img)
            self.msg_text.grid(row=1, column=1, rowspan=2, columnspan=2, sticky="nw", padx=(10,0), pady=(0,15))
        except Exception as e:
            print("Image message widget error: ", e)

# Custom widget to show file msg
class file_message_widget(tk.Frame): # DAWSON 2/13/2023
    def dl_attachment(self, path):
        dest_path = tkinter.filedialog.asksaveasfilename(initialfile=path.split('\\')[-1])
        print("Write to dir: ", dest_path)
        dest_file = open(dest_path, 'wb')
        src_file = open(path, 'rb')
        dest_file.write(src_file.read())
        dest_file.close()
        src_file.close()
    def __init__(self, parent, prof, username, path, datetime):
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

        self.attachment_button = ttk.Button(self, text="Attachment", command=lambda: self.dl_attachment(path))
        self.attachment_button.grid(row=1, column=1, rowspan=2, columnspan=2, sticky="nw", padx=(10,0), pady=(0,15))

# The entire App class
class App(tk.Tk):

    # Initialize ConnectionManager
    conman = None

    # Initialization function passed the net.hconnection object that handles Hermes connection states
    def __init__(self):
        super().__init__()

        # Setup ConnectionManager
        self.conman = ConnectionManager()
        self.username = "Dr_Wainwright"

        self.style = ttk.Style("cyborg")
        self.style.configure('TButton', background=PRIMARY_COLOR, bordercolor=PRIMARY_COLOR, lightcolor=PRIMARY_COLOR, darkcolor=PRIMARY_COLOR)
        self.style.map('TButton', background=[('disabled',PRIMARY_COLOR), ('active',PRIMARY_COLOR)])
        self.style.map('TButton', lightcolor=[('disabled',PRIMARY_COLOR), ('active',PRIMARY_COLOR)])
        self.style.map('TButton', bordercolor=[('disabled',PRIMARY_COLOR), ('active',PRIMARY_COLOR)])
        self.style.map('TButton', darkcolor=[('disabled',PRIMARY_COLOR), ('active',PRIMARY_COLOR)])

        self.style.configure("Gray.TButton",background='gray',bordercolor='gray',lightcolor='gray',darkcolor='gray')
        self.style.map('TButton', background=[('disabled','gray'), ('active','gray')])
        self.style.map('TButton', lightcolor=[('disabled','gray'), ('active','gray')])
        self.style.map('TButton', bordercolor=[('disabled','gray'), ('active','gray')])
        self.style.map('TButton', darkcolor=[('disabled','gray'), ('active','gray')])

        #Custom app window
        self.running = True
        self.overrideredirect(True)  # turns off default Windows titlebar

        self.title_bar = tk.Frame(self, bg="White", relief="raised", bd=3) # creates frame for new titlebar
        self.close_button = ttk.Button(self.title_bar, text=" X ", style="Cl.TButton", command=self.on_closing) # make closing button
        title_name = tk.Label(self.title_bar, text=APPNAME, bg=PRIMARY_COLOR, fg="white") # make window title

        self.title_bar.pack(side=tk.TOP, expand=True, fill=tk.X) # packing elements into main GUI window
        self.close_button.pack(side=tk.RIGHT)
        title_name.pack(side=tk.LEFT)

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
        if self.conman.isConnected():
            self.conman.close()
        self.quit()
        self.destroy()

    def connect(self, target, port):
        # NOTE TO FUTURE SELF: RENAME THIS FUNCTION BECAUSE ITS USED IN SERVER CLASSES
        # Takes a target and port and determines whether you're client or server
        # This will be changed in this future. Just needed something quick for sprint 2

        # Close existing connections
        if self.conman.isConnected():
            self.conman.close()

        self.target = target
        self.port = int(port)

        msg = "Would you like to open as server or client?"
        buttons = ["Server:primary", "Client"]
        mbox = Messagebox.show_question(msg, buttons=buttons, default="Server")

        if mbox == "Server":
            self.conman.createRoom(self.target, self.port)
        else:
            self.conman.connectToRoom(self.target, self.port)

        thread = threading.Thread(target=self.listen)
        thread.start()

    def listen(self):
        #This is run by a separate thread that is always looking for incoming messages and posts them to the texts
        while self.running:
            recv_msg = self.conman.getNextMessage()
            if recv_msg != None:
                self.parseMessage(recv_msg)
                self.canvas.update()
                self.canvas.yview_moveto(1.0)
        self.conman.close()

    def parseMessage(self, msg:Message):
        content = msg.getContent()
        # Message is a basic text message
        if msg.getHeader("message_type") == "message":
            d = datetime.datetime.now()
            message_widget(self.scrollable_frame, ASSETDIR+'\\'+USER1, msg.getHeader("username"), content, d).pack(anchor=tk.W)

        # Message is an image
        if msg.getHeader("message_type") == "image":
            d = datetime.datetime.now()
            img = open(".\\tmp\\" + str(uuid.uuid4()) + ".tmp", 'wb')
            img.write(base64.decodebytes(content[2:-1].encode('utf8')))
            print(img.name)
            image_message_widget(self.scrollable_frame, ASSETDIR+'\\'+USER1, msg.getHeader("username"), img.name, d).pack(anchor=tk.W)
            img.close()

        # Message is a file - DECLAN - make this get the file and show the download button
        if msg.getHeader("message_type") == "file": # DAWSON 2/13/2023
            d = datetime.datetime.now()
            file = open(".\\tmp\\" + str(uuid.uuid4()) + "." + msg.getHeader("ext"), 'wb')
            file.write(base64.decodebytes(content[2:-1].encode('utf8')))
            print(file.name)
            file_message_widget(self.scrollable_frame, ASSETDIR+'\\'+USER1, msg.getHeader("username"), file.name, d).pack(anchor=tk.W)
            file.close()

        # Message is a control message
        if msg.getHeader("message_type") == "control":
            if msg.getContent() == "SERVER CLOSE":
                self.running = False
                self.conman.close()
                print("Server Closed")

    def sendTextMessage(self, event=None):
        #Sends a message and adds it to the texts list
        msg = self.entry_field.get()
        if msg == "":
            return
        ecmsg = Message(msg)
        ecmsg.setHeader('username', self.username)
        ecmsg.setHeader('message_type','message')
        self.conman.sendMessage(ecmsg) #TESTING BY DAWSON
        self.entry_field.delete(0, tk.END)
        d = datetime.datetime.now()
        message_widget(self.scrollable_frame, ASSETDIR+'\\'+USER2, self.username, msg, d).pack(anchor=tk.W)
        self.canvas.update()
        self.canvas.yview_moveto(1.0)

    def sendImageMessage(self, path):

        image = open(path, 'rb')
        data = b''
        for line in image.readlines():
            data +=line
        #Sends a message and adds it to the texts list
        msg = self.entry_field.get()
        ecmsg = Message()
        ecmsg.setHeader('username', self.username)
        ecmsg.setHeader('message_type', 'image')
        ecmsg.setContent(str(base64.b64encode(data)))
        self.conman.sendMessage(ecmsg) #TESTING BY DAWSON
        self.entry_field.delete(0, tk.END)
        d = datetime.datetime.now()
        image_message_widget(self.scrollable_frame, ASSETDIR+'\\'+USER2, self.username, image.name, d).pack(anchor=tk.W)
        self.canvas.update()
        self.canvas.yview_moveto(1.0)
        image.close()

    def sendFileMessage(self, path): # DAWSON 2/13/2023

        file = open(path, 'rb')
        data = b''
        for line in file.readlines():
            data +=line
        #Sends a message and adds it to the texts list
        msg = self.entry_field.get()
        ecmsg = Message()
        ecmsg.setHeader('username', self.username)
        ecmsg.setHeader('message_type', 'file')
        ecmsg.setHeader('ext', file.name.split('.')[1])
        ecmsg.setContent(str(base64.b64encode(data)))
        self.conman.sendMessage(ecmsg) #TESTING BY DAWSON
        self.entry_field.delete(0, tk.END)
        d = datetime.datetime.now()
        file_message_widget(self.scrollable_frame, ASSETDIR+'\\'+USER2, self.username, file.name,d).pack(anchor=tk.W)
        self.canvas.update()
        self.canvas.yview_moveto(1.0)

    def addAttachment(self):
        file_path = tkinter.filedialog.askopenfilename(initialdir = "/", title = "Attachment",filetypes = (("all files","*.*"),("Text files","*.txt*")))
        print(file_path)
        if (file_path[-3:] == "jpg" or file_path[-3:] == "png"):
            self.sendImageMessage(file_path)
        else:
            self.sendFileMessage(file_path)

    def addEmoji(self):
        emopage = ttk.Toplevel()
        emopage.title(APPNAME)
        emopage.iconbitmap(ASSETDIR+'\\icon.ico')
        
        settings_label = ttk.Label(emopage, text="Insert Emoji", font=("OCBR", 20))
        settings_label.pack(pady=Y_PADDING)

        allEmoji = ["\U0001F603", "\U0001F602", "\U0001F609", "\U0001F970", "\U0001F618",
                    "\U0001F914", "\U0001F92B", "\U0001F644", "\U0001F634", "\U0001F922",
                    "\U0001F975", "\U0001F976", "\U00002639", "\U0001F44D", "\U0001F44E"]
        
        my_font = Font(family="Segoe UI Emoji", size = 25)

        emojiFrame = ttk.Frame(emopage)
        emojiFrame.pack(padx=10, pady=10)
        
        my_row = -1
        my_col = 0
        for emo in range(0,len(allEmoji)):
            if((emo % 5)==0):
                my_row += 1
                my_col = 0
            label = ttk.Label(emojiFrame, text=allEmoji[emo], font=my_font)
            label.grid(row=my_row, column=my_col, padx=5, pady=5)
            label.bind("<Button-1>")
            #label.bind("<Button-1>", lambda event: self.settings())
            my_col += 1

    def settings(self):
        top = ttk.Toplevel()
        top.title(APPNAME)
        top.iconbitmap(ASSETDIR+'\\icon.ico')
        top.resizable(False, False)

        settings_label = ttk.Label(top, text="Settings", font=("OCBR", 22))
        settings_label.pack(pady=Y_PADDING)

        username_frame = ttk.Frame(top)
        username_frame.pack(padx=X_PADDING, pady=Y_PADDING, fill=tk.X, expand=tk.YES)
        username_label = ttk.Label(username_frame, text="Username", font=FONT, width=15)
        username_label.pack(side=tk.LEFT, padx=(0,X_PADDING), pady=Y_PADDING)
        username_entry = ttk.Entry(username_frame, font=FONT)
        username_entry.insert(0, self.username)
        username_entry.pack(side=tk.RIGHT, fill=tk.X, expand=tk.YES)

        theme_frame = ttk.Frame(top)
        theme_frame.pack(padx=X_PADDING, pady=(0,Y_PADDING), fill=tk.X, expand=tk.YES)
        theme_label = ttk.Label(theme_frame, text="Theme", font=FONT, width=15)
        theme_label.pack(side=tk.LEFT, padx=(0,X_PADDING))
        style = ttk.Style()
        theme_names = style.theme_names()
        theme_cbo = ttk.Combobox(
            master=theme_frame,
            text=style.theme.name,
            values=theme_names,
            font=FONT,
        )
        theme_cbo.pack(side=tk.RIGHT, fill=tk.X, expand=tk.YES)
        theme_cbo.current(theme_names.index(style.theme.name))
        def change_theme(e):
            t = theme_cbo.get()
            self.style.theme_use(t)
            theme_cbo.selection_clear()
        theme_cbo.bind("<<ComboboxSelected>>", change_theme)

        prof_frame = ttk.Frame(top)
        prof_frame.pack(padx=X_PADDING, pady=(0,Y_PADDING), fill=tk.X, expand=tk.YES)
        prof_label = ttk.Label(prof_frame, text="Photo", font=FONT, width=15)
        prof_label.pack(side=tk.LEFT, padx=(0,X_PADDING))
        prof_button = ttk.Button(prof_frame, text="Select")
        prof_button.pack(side=tk.RIGHT, fill=tk.X, expand=tk.YES)

        # img_frame = ttk.Frame(top)
        # img_frame.pack(padx=X_PADDING, fill=tk.X, expand=tk.YES)
        # pic = Image.open(ASSETDIR+'\\'+USER1)
        # # pic = pic.resize(50,50)
        # pic = ImageTk.PhotoImage(pic)
        # pic_label = ttk.Label(img_frame, image=pic)
        # pic_label.pack(expand=tk.YES, fill=tk.BOTH)

    def bindings(self):
        self.bind('<Return>', self.sendTextMessage)
        self.title_bar.bind('<B1-Motion>', self.move_app)
        self.title_bar.bind('<Button-1>', self.get_pos)

    def get_pos(self, e):
        """Gets current position of cursor within the window"""
        global xwin
        global ywin
        xwin = e.x
        ywin = e.y

    def move_app(self, e):
        """Enables ability to move window around screen"""
        self.geometry(f'+{e.x_root - xwin}+{e.y_root - ywin}')

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
        self.canvas = tk.Canvas(texts_frame)
        self.scrollbar = ttk.Scrollbar(texts_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        #Send frame is where you enter and send texts
        send_frame = ttk.Frame()
        settings_button = ttk.Button(send_frame, text="Settings", command=lambda: self.settings())
        settings_button.pack(side=tk.LEFT, padx=(0,X_PADDING))
        my_msg = tk.StringVar()
        self.entry_field = ttk.Entry(send_frame, textvariable=my_msg, font=FONT)
        self.entry_field.pack(padx=(0,X_PADDING), side=tk.LEFT, fill=tk.X, expand=tk.TRUE)
        send_button = ttk.Button(send_frame, text="Send", command=lambda: self.sendTextMessage())
        send_button.pack(side=tk.RIGHT)
        attach_button = ttk.Button(send_frame, text="Attach File", command=self.addAttachment)
        attach_button.pack(side=tk.RIGHT, padx=(0,X_PADDING))
        attach_button = ttk.Button(send_frame, text="\U0001F603", command=self.addEmoji)
        attach_button.pack(side=tk.RIGHT, padx=(0,X_PADDING))
        send_frame.pack(padx=X_PADDING, pady=Y_PADDING, fill=tk.X)

if __name__ == "__main__":
    app = App()
    app.mainloop()
