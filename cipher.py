import argparse
import sys
import collections
import pickle
import os
import typing
from contextlib import contextmanager


def arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_encode = subparsers.add_parser("encode", help="Encode")
    parser_encode.set_defaults(code='encode')
    parser_encode.add_argument('--cipher', help="Type of cipher",
                               required=True)
    parser_encode.add_argument('--key', help="Key for cipher", required=True)
    parser_encode.add_argument('--input-file', help="Path to the input file",
                               required=False, default=sys.stdin)
    parser_encode.add_argument('--output-file', help="Path to the output file",
                               required=False, default=sys.stdout)

    parser_decode = subparsers.add_parser("decode", help="Decode")
    parser_decode.set_defaults(code='decode')
    parser_decode.add_argument('--cipher', help="Type of cipher")
    parser_decode.add_argument('--key', help="Key for cipher")
    parser_decode.add_argument('--input-file', help="Path to the input file",
                               required=False, default=sys.stdin)
    parser_decode.add_argument('--output-file', help="Path to the output file",
                               required=False, default=sys.stdout)

    parser_train = subparsers.add_parser("train", help="Train")
    parser_train.set_defaults(code='train')
    parser_train.add_argument('--text-file', help="Path to the input file",
                              required=False, default=sys.stdin)
    parser_train.add_argument('--model-file', help="Path to the model file",
                              required=True)

    parser_hack = subparsers.add_parser("hack", help="Hack")
    parser_hack.set_defaults(code='hack')
    parser_hack.add_argument('--input-file', help="Path to the input file",
                             required=False, default=sys.stdin)
    parser_hack.add_argument('--output-file', help="Path to the output file",
                             required=False, default=sys.stdout)
    parser_hack.add_argument('--model-file', help="Path to the model file",
                             required=True)

    args = parser.parse_args()

    return args


@contextmanager
def get_stream(file: typing.Any, mode: str) -> typing.Any:
    stream = file
    if stream not in (sys.stdin, sys.stdout):
        if os.path.exists(file):
            stream = open(file, mode)
        else:
            print("No such file in directory", file)
            sys.exit()
    yield stream
    if stream not in (sys.stdin, sys.stdout):
        stream.close()


def fileread(read_file: typing.Any) -> typing.List[str]:
    with get_stream(read_file, 'r') as infile:
        text = list(infile.read())
    return text


def textprint(output_file: typing.Any, text: typing.List[str]) -> None:
    with get_stream(output_file, 'w') as outfile:
        outfile.write("".join(text))


class Cipher:
    def encode(self, itter: typing.List[str]) -> typing.List[str]:
        pass

    def decode(self, itter: typing.List[str]) -> typing.List[str]:
        pass


class Caesar(Cipher):
    key: int
    alphabet: str = ("abcdefghijklmnopqrstuvwxyz"
                     "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                     "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
                     "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
                     "1234567890!?'(),.-:;_/")

    def encode(self, itter: typing.List[str]) -> typing.List[str]:
        decoded = []
        for chr in itter:
            if chr in self.alphabet:
                chr = self.alphabet[
                    (self.alphabet.find(chr) + self.key) % len(self.alphabet)
                    ]
            decoded.append(chr)
        return decoded

    def decode(self, itter: typing.List[str]) -> typing.List[str]:
        self.key *= -1
        return self.encode(itter)


class Vigenere(Cipher):
    key: str
    alphabet: str = ("abcdefghijklmnopqrstuvwxyz"
                     "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                     "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
                     "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
                     "1234567890!?'(),.-:;_/")

    def encode(self, itter: typing.List[str]) -> typing.List[str]:
        i = 0
        for letter in self.key:
            if letter not in self.alphabet:
                print("Key for vigenere should be a word")
                sys.exit()
        decoded = []
        for chr in itter:
            if chr in self.alphabet:
                chr = self.alphabet[
                    (self.alphabet.find(chr) +
                     self.alphabet.find(self.key[i])) % len(self.alphabet)
                    ]
                i = (i + 1) % len(self.key)
            decoded.append(chr)
        return decoded

    def decode(self, itter: typing.List[str]) -> typing.List[str]:
        myList = []
        for letter in self.key:
            myList.append(
                self.alphabet[-self.alphabet.find(letter)]
            )
        self.key = "".join(myList)
        return self.encode(itter)


class Vernam(Cipher):
    key: str
    alphabet = {
        "A": "10000",
        "B": "00110",
        "C": "10110",
        "D": "11110",
        "E": "01000",
        "F": "01110",
        "G": "01010",
        "H": "11010",
        "I": "01100",
        "J": "10010",
        "K": "10011",
        "L": "11011",
        "M": "01011",
        "N": "01111",
        "O": "11100",
        "P": "11111",
        "Q": "10111",
        "R": "00111",
        "S": "00101",
        "T": "10101",
        "U": "10100",
        "V": "11101",
        "W": "01101",
        "X": "01001",
        "Y": "00100",
        "Z": "11001",
        "'": "11000",
        "-": "00000",
        ":": "00011",
        ".": "00010",
        ",": "00001",
        "/": "10001"
    }

    @staticmethod
    def xor(str1: str, str2: str) -> str:
        new_str = ""
        for i in range(5):
            new_str += str(
                (int(str1[i]) + int(str2[i])) % 2
            )
        return new_str

    def encode(self, itter: typing.List[str]) -> typing.List[str]:
        self.key = self.key.upper()
        new_itter = []
        ind = 0
        vernam = Vernam()
        for letter in itter:
            if letter.upper() not in self.alphabet:
                new_itter.append(letter)
                continue
            vernam.key = self.key
            coded = vernam.xor(
                self.alphabet[letter.upper()],
                self.alphabet[self.key[ind % len(self.key)]]
            )
            for item in self.alphabet:
                if self.alphabet[item] == coded:
                    letter = item
            new_itter.append(letter)
            ind += 1
        return new_itter

    def decode(self, itter: typing.List[str]) -> typing.List[str]:
        return self.encode(itter)


class FreqAnalysis:
    model_file: str
    alphabet: str = ("abcdefghijklmnopqrstuvwxyz"
                     "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                     "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
                     "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
                     "1234567890!?'(),.-:;_/")

    def __init__(self, new_model_file: str) -> None:
        self.model_file = new_model_file

    def train(self, itter: typing.List[str]) -> None:
        myDict = collections.Counter(
            item.lower() for item in itter if item in self.alphabet
        )
        alphaNums = sum(myDict.values())
        if alphaNums == 0:
            print("Text-file should contain letters")
            sys.exit()
        onlyAlpha = {}
        for item in myDict:
            onlyAlpha[item] = myDict[item] / alphaNums
        with get_stream(self.model_file, 'wb') as pickle_file:
            pickle.dump(onlyAlpha, pickle_file)

    def hack(self, itter: typing.List[str]) -> typing.List[str]:
        with get_stream(self.model_file, 'rb') as pickle_file:
            myDict = pickle.load(pickle_file)
        alphaNums = sum(collections.Counter(itter).values())
        if alphaNums == 0:
            print("Model-file should contain letters")
            sys.exit()
        minMeas = 100
        key = 1
        keyMin = 0
        caesar = Caesar()
        while key <= 25:
            measure = 0
            caesar.key = key
            newItter = caesar.decode(itter)
            itterDict = collections.Counter(
                item.lower() for item in newItter
                if item in self.alphabet
            )
            for item in myDict:
                measure += abs(myDict[item] - itterDict[item] / alphaNums)
            if measure < minMeas:
                minMeas = measure
                keyMin = key
            key += 1
        caesar.key = keyMin
        return caesar.decode(itter)


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
