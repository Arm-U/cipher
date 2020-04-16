import argparse
import string
import sys
import collections
import pickle


def Parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("code")
    parser.add_argument('--cipher')
    parser.add_argument('--key')
    parser.add_argument('--input-file')
    parser.add_argument('--output-file')
    parser.add_argument('--model-file')
    parser.add_argument('--text-file')
    args = parser.parse_args()
    return args


def fileread(args) -> list:
    if args.code != "train":
        if args.input_file == None:
            infile = sys.stdin
        else:
            infile = open(args.input_file, 'r')
        text = []
        for lines in infile.readlines():
            for symbols in lines:
                text.append(symbols)
    else:
        if args.text_file == None:
            infile = sys.stdin
        else:
            infile = open(args.text_file, 'r')
        text = []
        for lines in infile.readlines():
            for symbols in lines:
                text.append(symbols)
    infile.close()
    return text


def textprint(output_file, text: list):
    if output_file == None:
        outfile = sys.stdout
    else:
        outfile = open(output_file, 'w')
    for letter in text:
        outfile.write(letter)
    outfile.close()


class Encode:
    def caesar(key: int, itter: list) -> list:
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

    def vigenre(key: str, itter: list) -> list:
        i = 0
        key = key.lower()
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


class Decode:
    def caesar(key: int, itter: list) -> list:
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

    def vigenre(key: str, itter: list) -> list:
        i = 0
        key = key.lower()
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


class Train:
    def train(itter: list, model_file: str):
        myDict = collections.Counter(itter)
        alphaNums = 0
        for item in myDict:
            if item in string.ascii_letters:
                alphaNums += 1
        onlyAlpha = {}
        for item in myDict:
            if item in string.ascii_letters:
                onlyAlpha[item] = myDict[item] / alphaNums
        with open(model_file, 'wb') as pickle_file:
            pickle.dump(onlyAlpha, pickle_file)
        return;


class Hack:
    def hack(itter: list, model_file: str):
        with open(model_file, 'rb') as pickle_file:
            myDict = pickle.load(pickle_file)
        alphaNums = 0
        for item in myDict:
            if item in string.ascii_letters:
                alphaNums += 1
        minMeas = 100
        key = 1
        keyMin = 0
        while key <= 25:
            measure = 0
            newItter = Decode.caesar(key, itter)
            itterDict = collections.Counter(newItter)
            for item in myDict:
                measure += abs(myDict[item] - itterDict[item] / alphaNums)
            if measure < minMeas:
                minMeas = measure
                keyMin = key
            key += 1
        return Decode.caesar(keyMin, itter)


def Code(args):
    text = fileread(args)
    if args.code == 'encode':
        if args.cipher == 'caesar':
            dec_text = Encode.caesar(int(args.key), text)
            textprint(args.output_file, dec_text)
        elif args.cipher == 'vigenre':
            dec_text = Encode.vigenre(args.key, text)
            textprint(args.output_file, dec_text)
    elif args.code == 'decode':
        if args.cipher == 'caesar':
            dec_text = Decode.caesar(int(args.key), text)
            textprint(args.output_file, dec_text)
        elif args.cipher == 'vigenre':
            dec_text = Decode.vigenre(args.key, text)
            textprint(args.output_file, dec_text)
    elif args.code == 'train':
        Train.train(text, args.model_file)
    elif args.code == 'hack':
        dec_text = Hack.hack(text, args.model_file)
        textprint(args.output_file, dec_text)


args = Parser()
Code(args)
