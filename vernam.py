from cipher import Cipher
import typing


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
