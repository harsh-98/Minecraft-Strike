import argparse
from minecraft_strike.server import start_server
from minecraft_strike.client import start_client
parser = argparse.ArgumentParser(description='Optional app description')


def main():
    parser.add_argument('--server', action='store_true',
                    help='A boolean switch')

    args = parser.parse_args()
    {
        True: start_server,
        False: start_client
    }.get(args.server)()
