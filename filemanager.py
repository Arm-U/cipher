from contextlib import contextmanager
import typing
import sys
import os


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
