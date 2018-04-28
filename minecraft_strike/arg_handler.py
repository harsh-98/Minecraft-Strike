import argparse
from minecraft_strike.server import start_server
from minecraft_strike.client import start_client
parser = argparse.ArgumentParser(description='Optional app description')


def main():
    parser.add_argument('--server', action='start_server',
                    help='A boolean switch')
    parser.add_argument('--client', action='start_client',
                    help='A boolean switch')
