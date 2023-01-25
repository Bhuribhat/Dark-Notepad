import argparse

from notepad import Notepad

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', help='your name', type=str)
parser.add_argument('-m', '--mail', help='email address', type=str)
parser.add_argument('-p', '--phone', help='phone number', type=str)
parser.add_argument('-s', '--social', help='social media contract', type=str)
args = parser.parse_args()


if __name__ == '__main__':
    APP = Notepad(
        name=args.name, mail=args.mail, 
        phone=args.phone, social=args.social
    )
    APP.run()