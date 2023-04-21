import argparse
import os
from chat import Chat as chat
from gui.app import App
__BANNER__ = """Encrypted Chat v1.0"""

NATIVEDIR = os.path.dirname(os.path.abspath(__name__))
CONFIGDIR = os.path.join(NATIVEDIR, "conf")

def main():
    # Prints the banner
    print(__BANNER__)
  
    path = os.path.join(NATIVEDIR, "tmp")
    if(not os.path.exists(path)):
        os.mkdir(path)
    if(not os.path.exists(CONFIGDIR)):
        os.mkdir(CONFIGDIR)
    if(not os.path.exists(NATIVEDIR + '\\conf\\config.txt')):
        prof = open(NATIVEDIR+"\\assets\prof1.jpg",'rb')
        prof2 = open(CONFIGDIR + "\\prof1.jpg",'wb+')
        for line in prof.readlines():
            prof2.write(line)
        prof2.close()
        file = open(CONFIGDIR +"\\config.txt",'w+')
        file.close()
    
    # Creates an ArgumentParser object with the name and description of the program
    parser = argparse.ArgumentParser(prog='EncryptedChat.py', description='Encrypted Chat Program')
    
    # Adds a sub-parser to the main parser
    # The 'dest' attribute specifies the name of the attribute that will be added to the namespace
    subparser = parser.add_subparsers(dest='mode')
    client = subparser.add_parser('client')
    host   = subparser.add_parser('host')
    gui    = subparser.add_parser('gui')

    # Adds 'ip' and 'port' arguments to the 'client' parser
    client.add_argument('--ip', '-i', type=str, nargs=1, help='Designates server ip address.')
    client.add_argument('--port', '-p', type=int, nargs=1, help='Designates server destination port.')
    
    # Adds 'ip' and 'port' arguments to the 'host' parser
    host.add_argument('--ip', '-i', type=str, nargs=1, help='Designates local bind ip address.')
    host.add_argument('--port', '-p', type=int, nargs=1, help='Designates server local bind port.')
    
    # Parses the command line arguments
    args = parser.parse_args()

    # If the mode is 'client'
    if args.mode == 'client':
        print("[+] Attempting connection in client mode.")

        if chat.client_mode() == False:
            
            # If the connection fails, defaults to server mode
            print("[-] Connection failed, defaulting to server mode.")
            chat.server_mode()

    if args.mode == 'host':
        # Runs the server mode
        chat.server_mode()
        
    if args.mode == 'gui':
        print("GUI Mode")
        app = App()
        
        # Runs the main loop of the app
        app.mainloop()
        
    # If the mode is not specified
    else:
        # Prints a message
        print("GUI Mode")
        
        # Creates an App object with the username
        app = App()
        
        # Runs the main loop of the app
        app.mainloop()

# If the script is run as the main program
if __name__ == '__main__':
    main()
