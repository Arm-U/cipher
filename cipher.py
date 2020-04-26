import argparse
import string
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


class Caesar:
    key: int

    def __init__(self, new_key: int) -> None:
        self.key = new_key

    def encode(self, itter: typing.List[str]) -> typing.List[str]:
        decoded = []
        for chr in itter:
            if chr in string.ascii_lowercase:
                chr = string.ascii_lowercase[
                    (string.ascii_lowercase.find(chr) + self.key) % 26
                    ]
            if chr in string.ascii_uppercase:
                chr = string.ascii_uppercase[
                    (string.ascii_uppercase.find(chr) + self.key) % 26
                    ]
            decoded.append(chr)
        return decoded

    def decode(self, itter: typing.List[str]) -> typing.List[str]:
        self.key *= -1
        return Caesar(self.key).encode(itter)


class Vigenere:
    key: str

    def __init__(self, new_key: str) -> None:
        self.key = new_key

    def encode(self, itter: typing.List[str]) -> typing.List[str]:
        i = 0
        self.key = self.key.lower()
        for letter in self.key:
            if letter not in string.ascii_letters:
                print("Key for vigenere should be a word")
                sys.exit()
        decoded = []
        for chr in itter:
            if chr in string.ascii_lowercase:
                chr = string.ascii_lowercase[
                    (string.ascii_lowercase.find(chr) +
                     string.ascii_lowercase.find(self.key[i])) % 26
                    ]
                i = (i + 1) % len(self.key)
            if chr in string.ascii_uppercase:
                chr = string.ascii_uppercase[
                    (string.ascii_uppercase.find(chr) +
                     string.ascii_lowercase.find(self.key[i])) % 26
                    ]
                i = (i + 1) % len(self.key)
            decoded.append(chr)
        return decoded

    def decode(self, itter: typing.List[str]) -> typing.List[str]:
        myList = []
        self.key = self.key.lower()
        for letter in self.key:
            myList.append(
                string.ascii_lowercase[-string.ascii_lowercase.find(letter)]
            )
        self.key = "".join(myList)
        return Vigenere(self.key).encode(itter)


class FreqAnalysis:
    model_file: str

    def __init__(self, new_model_file: str) -> None:
        self.model_file = new_model_file

    def train(self, itter: typing.List[str]) -> None:
        myDict = collections.Counter(
            item.lower() for item in itter if item in string.ascii_letters
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
        while key <= 25:
            measure = 0
            newItter = Caesar(key).decode(itter)
            itterDict = collections.Counter(
                item.lower() for item in newItter
                if item in string.ascii_letters
            )
            for item in myDict:
                measure += abs(myDict[item] - itterDict[item] / alphaNums)
            if measure < minMeas:
                minMeas = measure
                keyMin = key
            key += 1
        return Caesar(keyMin).decode(itter)


def code(args: argparse.Namespace) -> None:
    if args.code == 'encode':
        text = fileread(args.input_file)
        if args.cipher == 'caesar':
            try:
                key_int = int(args.key)
            except ValueError:
                print("Key for caesar should be integer")
                sys.exit()
            textprint(args.output_file, Caesar(key_int).encode(text))
        elif args.cipher == 'vigenere':
            textprint(args.output_file, Vigenere(args.key).encode(text))
        else:
            print("Sorry i don't know this kind of cipher:", args.cipher)
            sys.exit()
    elif args.code == 'decode':
        text = fileread(args.input_file)
        if args.cipher == 'caesar':
            try:
                key_int = int(args.key)
            except ValueError:
                print("Key for caesar should be integer")
                sys.exit()
            textprint(args.output_file, Caesar(key_int).decode(text))
        elif args.cipher == 'vigenere':
            textprint(args.output_file, Vigenere(args.key).decode(text))
        else:
            print("Sorry i don't know this kind of cipher:", args.cipher)
            sys.exit()
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
