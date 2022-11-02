import argparse
import sys
from chat import Cli

__BANNER__ = """Encrypted Chat v1.0"""

def main():
    print(__BANNER__)
    parser = argparse.ArgumentParser(prog='EncryptedChat.py', description='Encrypted Chat Program')
    subparser = parser.add_subparsers(dest='mode')

    client = subparser.add_parser('client')
    host   = subparser.add_parser('host')
    gui    = subparser.add_parser('gui')

    #check if there are no arguments (just running the main method)
    if not (len(sys.argv) > 1):
        parser.print_help()

    client.add_argument('--ip', '-i', type=str, nargs=1, help='Designates server ip address.')
    client.add_argument('--port', '-p', type=int, nargs=1, help='Designates server destination port.')
    host.add_argument('--ip', '-i', type=str, nargs=1, help='Designates local bind ip address.')
    host.add_argument('--port', '-p', type=int, nargs=1, help='Designates server local bind port.')

    args = parser.parse_args()

    if not (len(args) > 1):
        parser.print_help()

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
