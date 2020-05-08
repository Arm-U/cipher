from caesar import Caesar
from filemanager import get_stream
import pickle
import collections
import typing
import sys


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
