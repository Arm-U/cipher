from cipher import Cipher
from caesar import Caesar
from vigenere import Vigenere
from vernam import Vernam
from freqanalysis import FreqAnalysis
from filemanager import fileread
from filemanager import textprint
from parser import arg_parser
import sys
import argparse


def code(args: argparse.Namespace) -> None:
    if not hasattr(args, 'code'):
        print("Enter something to do: encode, decode, train, hack")
        sys.exit()

    if args.code in ('encode', 'decode'):
        text = fileread(args.input_file)
        cipher = Cipher()
        if args.cipher == 'caesar':
            try:
                key_int = int(args.key)
            except ValueError:
                print("Key for caesar should be integer")
                sys.exit()
            cipher = Caesar()
            cipher.key = key_int
        elif args.cipher == 'vigenere':
            cipher = Vigenere()
            cipher.key = args.key
        elif args.cipher == 'vernam':
            cipher = Vernam()
            cipher.key = args.key
        else:
            print("No such cipher type")
            sys.exit()
        if args.code == 'encode':
            textprint(args.output_file, cipher.encode(text))
        else:
            textprint(args.output_file, cipher.decode(text))
    elif args.code == 'train':
        FreqAnalysis(args.model_file).train(fileread(args.text_file))
    elif args.code == 'hack':
        text = fileread(args.input_file)
        textprint(args.output_file, FreqAnalysis(args.model_file).hack(text))


def main() -> None:
    args = arg_parser()
    code(args)


if __name__ == '__main__':
    main()
