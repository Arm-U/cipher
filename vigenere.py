from cipher import Cipher
import typing
import sys


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
        original_key = self.key
        self.key = "".join(myList)
        result = self.encode(itter)
        self.key = original_key
        return result
