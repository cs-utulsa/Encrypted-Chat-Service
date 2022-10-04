import argparse
from chat import Cli

__BANNER__ = """Encrypted Chat v1.0"""

def main():
    print(__BANNER__)
    parser = argparse.ArgumentParser(prog='EncryptedChat.py', description='Encrypted Chat Program')
    subparser = parser.add_subparsers(dest='mode')

    client = subparser.add_parser('client')
    host   = subparser.add_parser('host')
    gui    = subparser.add_parser('gui')

    client.add_argument('--target', metavar='-t', type=str, nargs=1, help='Designates server ip address.')
    client.add_argument('--port', metavar='-p', type=int, nargs=1, help='Designates server destination port.')
    host.add_argument('--local-ip', metavar='-l', type=str, nargs=1, help='Designates local bind ip address.')
    host.add_argument('--port', metavar='-p', type=int, nargs=1, help='Designates server local bind port.')
    args = parser.parse_args()
    _cli = Cli(args)

    if args.mode == 'client':
        _cli.client_mode()
    if args.mode == 'server':
        # TODO Server mode.
        _cli.server_mode()
    if args.mode == 'gui':
        # TODO GUI mode.
        print("GUI Mode")


if __name__ == '__main__':
    main()
