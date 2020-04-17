import argparse
import string
import sys
import collections
import pickle
import os


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


def fileread(args: argparse.Namespace) -> list:
    if args.code == "encode" or args.code == "decode" or args.code == "hack":
        if args.input_file is None:
            infile = sys.stdin
        else:
            try:
                if os.path.exists(args.input_file):
                    infile = open(args.input_file, 'r')
                else:
                    raise Exception()
            except Exception:
                print("No such file in directory:", args.input_file)
                sys.exit()
    elif args.code == "train":
        if args.text_file is None:
            infile = sys.stdin
        else:
            try:
                if os.path.exists(args.text_file):
                    infile = open(args.text_file, 'r')
                else:
                    raise Exception()
            except Exception:
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


def textprint(output_file: str, text: list) -> None:
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
    def encode(key: int, itter: list) -> list:
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
    def decode(key: int, itter: list) -> list:
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


class Vigenre:
    @staticmethod
    def encode(key: str, itter: list) -> list:
        i = 0
        key = key.lower()
        for letter in key:
            if letter not in string.ascii_letters:
                print("Key for vigenre should be a word")
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
    def decode(key: str, itter: list) -> list:
        i = 0
        key = key.lower()
        for letter in key:
            if letter not in string.ascii_letters:
                print("Key for vigenre should be a word")
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
    def train(itter: list, model_file: str) -> None:
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
    def hack(itter: list, model_file: str) -> list:
        try:
            if not os.path.exists(model_file):
                raise Exception()
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


def Code(args: argparse.Namespace) -> None:
    text = fileread(args)
    if args.code == 'encode':
        if args.cipher == 'caesar':
            try:
                dec_text = Caesar.encode(int(args.key), text)
                textprint(args.output_file, dec_text)
            except ValueError:
                print("Key for caesar should be integer")
        elif args.cipher == 'vigenre':
            dec_text = Vigenre.encode(args.key, text)
            textprint(args.output_file, dec_text)
        else:
            print("Sorry i don't know this kind of cipher:", args.cipher)
    elif args.code == 'decode':
        if args.cipher == 'caesar':
            try:
                dec_text = Caesar.decode(int(args.key), text)
                textprint(args.output_file, dec_text)
            except ValueError:
                print("Key for caesar should be integer")
        elif args.cipher == 'vigenre':
            dec_text = Vigenre.decode(args.key, text)
            textprint(args.output_file, dec_text)
        else:
            print("Sorry i don't know this kind of cipher:", args.cipher)
    elif args.code == 'train':
        FreqAnalysis.train(text, args.model_file)
    elif args.code == 'hack':
        dec_text = FreqAnalysis.hack(text, args.model_file)
        textprint(args.output_file, dec_text)


args = Parser()
Code(args)
