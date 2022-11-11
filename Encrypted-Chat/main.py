import argparse
import ipaddress
import sys
from chat import Cli

__BANNER__ = """Encrypted Chat v1.0"""

def main():
    """
    #printing the banner
    #creating the parser
    """
    print(__BANNER__)
    parser = argparse.ArgumentParser(prog='EncryptedChat.py', description='Encrypted Chat Program')
    subparser = parser.add_subparsers(dest='mode')
    
    """
    #check if there are no arguments (just running the main method)
    """
    if not (len(sys.argv) > 1):
        parser.print_help()

    client = subparser.add_parser('client')
    host   = subparser.add_parser('host')
    gui    = subparser.add_parser('gui')
    
    """
    #get the input for ip and port in client and host modes
    """
    client.add_argument('--ip', '-i', type=str, nargs=1, help='Designates server ip address.')
    client.add_argument('--port', '-p', type=int, nargs=1, help='Designates server destination port.')
    host.add_argument('--ip', '-i', type=str, nargs=1, help='Designates local bind ip address.')
    host.add_argument('--port', '-p', type=int, nargs=1, help='Designates server local bind port.')
    
    args = parser.parse_args()

    """
    Check for valid Ip address and port
    Shouldn't need it because the GUI should take care of this error
    """
    try:
        target = args.ip[0]
        ipaddress.IPv4Address(target)
    except ipaddress.AddressValueError:
        print('Please input accurate Ip address')
        exit()
    
    if (65535 < args.port[0] < 0):
        print('Invalid port')
        exit()
    
    _cli = Cli(args)

    """
    #call each modes based on the inputs
    """
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
