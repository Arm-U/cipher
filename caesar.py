from cipher import Cipher
import typing


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
        result = self.encode(itter)
        self.key *= -1
        return result
