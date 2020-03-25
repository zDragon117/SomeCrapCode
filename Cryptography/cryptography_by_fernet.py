import argparse

from cryptography.fernet import Fernet

# Create the parser
my_parser = argparse.ArgumentParser()

# Add the arguments
my_parser.add_argument('-m',
                       '--mode',
                       choices=['encrypt', 'decrypt'],
                       required=True,
                       help='Encrypt or Decrypt mode')

my_parser.add_argument('-k',
                       '--key',
                       required=True,
                       help='FERNET key require for encrypt and decrypt')

my_parser.add_argument('string',
                       metavar='string',
                       type=str,
                       help='String need to encrypt or decrypt')

# Execute the parse_args() method
args = my_parser.parse_args()


def encrypt(key, raw_string):
    key = bytes(key, "utf-8")
    b_str = bytes(raw_string, "utf-8")
    f = Fernet(key)
    return bytes.decode(f.encrypt(b_str), "utf-8")


def decrypt(key, cipher_text):
    key = bytes(key, "utf-8")
    b_str = bytes(cipher_text, "utf-8")
    f = Fernet(key)
    return bytes.decode(f.decrypt(b_str), "utf-8")


if __name__ == '__main__':
    if args.mode == 'encrypt':
        print('Encrypted text:', encrypt(args.key, args.string))
    elif args.mode == 'decrypt':
        print('Decrypted text:', decrypt(args.key, args.string))