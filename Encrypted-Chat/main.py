import argparse
import sys
from chat import Cli

__BANNER__ = """Encrypted Chat v1.0"""

def main():
    print(__BANNER__)
    parser = argparse.ArgumentParser(prog='EncryptedChat.py', description='Encrypted Chat Program')
    subparser = parser.add_subparsers(dest='mode')

    #parse each modes
    client = subparser.add_parser('client')
    host   = subparser.add_parser('host')
    gui    = subparser.add_parser('gui')

    #check if there are no arguments (just running the main method)
    if not (len(sys.argv) > 1):
        parser.print_help()
    
    #parse the ip and port for both client and host
    client.add_argument('--ip', '-i', type=str, nargs=1, help='Designates server ip address.')
    client.add_argument('--port', '-p', type=int, nargs=1, help='Designates server destination port.')
    host.add_argument('--ip', '-i', type=str, nargs=1, help='Designates local bind ip address.')
    host.add_argument('--port', '-p', type=int, nargs=1, help='Designates server local bind port.')

    #handles all/general errors if the inputs are incomplete
    client.error(client.print_help())
    host.error(client.print_help())

    args = parser.parse_args()
    
    _cli = Cli(args)

    if args.mode == 'client':
        print("[+] Attempting connection in client mode.")
        if _cli.client_mode() == False:
            print("[-] Connection failed, defaulting to server mode.")
            _cli.server_mode()
    if args.mode == 'host':
        # TODO Server mode.
        _cli.server_mode()
    if args.mode == 'gui':
        # TODO GUI mode.
        print("GUI Mode")


if __name__ == '__main__':
    main()
