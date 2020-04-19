import argparse
import string
import sys
import collections
import pickle
import os
import typing


def Parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("code", help="What to do")
    parser.add_argument('--cipher', help="Type of cipher")
    parser.add_argument('--key', help="Key for cipher")
    parser.add_argument('--input-file', help="Path to the input file")
    parser.add_argument('--output-file', help="Path to the output file")
    parser.add_argument('--model-file', help="Path to the model file")
    parser.add_argument('--text-file', help="Path to the input file")
    args = parser.parse_args()
    return args


def fileread(args: argparse.Namespace) -> typing.List[str]:
    if args.code in ("encode", "decode", "hack"):
        if args.input_file is None:
            infile = sys.stdin
        else:
            try:
                infile = open(args.input_file, 'r')
            except FileNotFoundError:
                print("No such file in directory:", args.input_file)
                sys.exit()
    elif args.code == "train":
        if args.text_file is None:
            infile = sys.stdin
        else:
            try:
                infile = open(args.text_file, 'r')
            except FileNotFoundError:
                print("No such file in directory", args.text_file)
                sys.exit()
    else:
        print("Sorry, I can’t complete this action:", args.code)
        print("I can do this actions:", end=" ")
        print("'encode', 'decode', 'train', 'hack'")
        sys.exit()
    text = []
    for lines in infile.readlines():
        for symbols in lines:
            text.append(symbols)
    infile.close()
    return text


def textprint(output_file: str, text: typing.List[str]) -> None:
    if output_file is None:
        outfile = sys.stdout
    else:
        try:
            if os.path.exists(output_file):
                outfile = open(output_file, 'w')
            else:
                raise Exception()
        except Exception:
            print("No such file in directory:", output_file)
            sys.exit()
    for letter in text:
        outfile.write(letter)
    outfile.close()


class Caesar:
    @staticmethod
    def encode(key: int, itter: typing.List[str]) -> typing.List[str]:
        decoded = []
        for chr in itter:
            if chr in string.ascii_lowercase:
                chr = string.ascii_lowercase[
                    (string.ascii_lowercase.find(chr) + key) % 26
                    ]
            if chr in string.ascii_uppercase:
                chr = string.ascii_uppercase[
                    (string.ascii_uppercase.find(chr) + key) % 26
                    ]
            decoded.append(chr)
        return decoded

    @staticmethod
    def decode(key: int, itter: typing.List[str]) -> typing.List[str]:
        coded = []
        for chr in itter:
            if chr in string.ascii_lowercase:
                chr = string.ascii_lowercase[
                    (string.ascii_lowercase.find(chr) - key) % 26
                    ]
            if chr in string.ascii_uppercase:
                chr = string.ascii_uppercase[
                    (string.ascii_uppercase.find(chr) - key) % 26
                    ]
            coded.append(chr)
        return coded


class Vigenere:
    @staticmethod
    def encode(key: str, itter: typing.List[str]) -> typing.List[str]:
        i = 0
        key = key.lower()
        for letter in key:
            if letter not in string.ascii_letters:
                print("Key for vigenere should be a word")
                sys.exit()
        decoded = []
        for chr in itter:
            if chr in string.ascii_lowercase:
                chr = string.ascii_lowercase[
                    (string.ascii_lowercase.find(chr) +
                     string.ascii_lowercase.find(key[i])) % 26
                    ]
                i = (i + 1) % len(key)
            if chr in string.ascii_uppercase:
                chr = string.ascii_uppercase[
                    (string.ascii_uppercase.find(chr) +
                     string.ascii_lowercase.find(key[i])) % 26
                    ]
                i = (i + 1) % len(key)
            decoded.append(chr)
        return decoded

    @staticmethod
    def decode(key: str, itter: typing.List[str]) -> typing.List[str]:
        i = 0
        key = key.lower()
        for letter in key:
            if letter not in string.ascii_letters:
                print("Key for vigenere should be a word")
                sys.exit()
        coded = []
        for chr in itter:
            if chr in string.ascii_lowercase:
                chr = string.ascii_lowercase[
                    (string.ascii_lowercase.find(chr) + 26 -
                     string.ascii_lowercase.find(key[i])) % 26
                    ]
                i = (i + 1) % len(key)
            if chr in string.ascii_uppercase:
                chr = string.ascii_uppercase[
                    (string.ascii_uppercase.find(chr) + 26 -
                     string.ascii_lowercase.find(key[i])) % 26
                    ]
                i = (i + 1) % len(key)
            coded.append(chr)
        return coded


class FreqAnalysis:
    @staticmethod
    def train(itter: typing.List[str], model_file: str) -> None:
        myDict = collections.Counter(itter)
        alphaNums = 0
        for item in myDict:
            if item in string.ascii_letters:
                alphaNums += 1
        onlyAlpha = {}
        for item in myDict:
            if item in string.ascii_letters:
                onlyAlpha[item] = myDict[item] / alphaNums
        try:
            if not os.path.exists(model_file):
                raise Exception()
            with open(model_file, 'wb') as pickle_file:
                pickle.dump(onlyAlpha, pickle_file)
        except Exception:
            print("No such file in directory:", model_file)
            sys.exit()

    @staticmethod
    def hack(itter: typing.List[str], model_file: str) -> list:
        try:
            with open(model_file, 'rb') as pickle_file:
                myDict = pickle.load(pickle_file)
        except Exception:
            print("No such file in directory:", model_file)
            sys.exit()
        alphaNums = 0
        for item in myDict:
            if item in string.ascii_letters:
                alphaNums += 1
        minMeas = 100
        key = 1
        keyMin = 0
        while key <= 25:
            measure = 0
            newItter = Caesar.decode(key, itter)
            itterDict = collections.Counter(newItter)
            for item in myDict:
                measure += abs(myDict[item] - itterDict[item] / alphaNums)
            if measure < minMeas:
                minMeas = measure
                keyMin = key
            key += 1
        return Caesar.decode(keyMin, itter)


def code(args: argparse.Namespace) -> None:
    text = fileread(args)
    if args.code == 'encode':
        if args.cipher == 'caesar':
            try:
                key_int = int(args.key)
            except ValueError:
                print("Key for caesar should be integer")
                sys.exit()
            dec_text = Caesar.encode(key_int, text)
            textprint(args.output_file, dec_text)
        elif args.cipher == 'vigenere':
            dec_text = Vigenere.encode(args.key, text)
            textprint(args.output_file, dec_text)
        else:
            print("Sorry i don't know this kind of cipher:", args.cipher)
            sys.exit()
    elif args.code == 'decode':
        if args.cipher == 'caesar':
            try:
                key_int = int(args.key)
            except ValueError:
                print("Key for caesar should be integer")
                sys.exit()
            dec_text = Caesar.decode(key_int, text)
            textprint(args.output_file, dec_text)
        elif args.cipher == 'vigenere':
            dec_text = Vigenere.decode(args.key, text)
            textprint(args.output_file, dec_text)
        else:
            print("Sorry i don't know this kind of cipher:", args.cipher)
            sys.exit()
    elif args.code == 'train':
        FreqAnalysis.train(text, args.model_file)
    elif args.code == 'hack':
        dec_text = FreqAnalysis.hack(text, args.model_file)
        textprint(args.output_file, dec_text)


def main() -> None:
    args = Parser()
    code(args)


if __name__ == '__main__':
    main()
