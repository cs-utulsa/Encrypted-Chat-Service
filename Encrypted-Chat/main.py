import argparse
from chat import Chat
from App import App
__BANNER__ = """Encrypted Chat v1.0"""

def main():
    print(__BANNER__)
    parser = argparse.ArgumentParser(prog='EncryptedChat.py', description='Encrypted Chat Program')
    subparser = parser.add_subparsers(dest='mode')

    client = subparser.add_parser('client')
    host   = subparser.add_parser('host')
    gui    = subparser.add_parser('gui')

    client.add_argument('--ip', '-i', type=str, nargs=1, help='Designates server ip address.')
    client.add_argument('--port', '-p', type=int, nargs=1, help='Designates server destination port.')
    host.add_argument('--ip', '-i', type=str, nargs=1, help='Designates local bind ip address.')
    host.add_argument('--port', '-p', type=int, nargs=1, help='Designates server local bind port.')
    args = parser.parse_args()
    chat = Chat(args)

    if args.mode == 'client':
        print("[+] Attempting connection in client mode.")
        if chat.client_mode() == False:
            print("[-] Connection failed, defaulting to server mode.")
            chat.server_mode()
    if args.mode == 'host':
        chat.server_mode()
    if args.mode == 'gui':
        print("GUI Mode")
        app = App()
        app.mainloop()
    else:
        print("GUI Mode")
        app = App()
        app.mainloop()


if __name__ == '__main__':
    main()
