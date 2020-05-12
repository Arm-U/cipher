from contextlib import contextmanager
import typing
import sys


@contextmanager
def get_stream(file: typing.Any, mode: str) -> typing.Any:
    stream = file
    if stream not in (sys.stdin, sys.stdout):
        stream = open(file, mode)
    try:
        yield stream
    finally:
        if stream not in (sys.stdin, sys.stdout):
            stream.close()


def fileread(read_file: typing.Any) -> typing.List[str]:
    try:
        with get_stream(read_file, 'r') as infile:
            text = list(infile.read())
    except FileNotFoundError:
        print("No such file in directory", read_file)
        sys.exit()
    return text


def textprint(output_file: typing.Any, text: typing.List[str]) -> None:
    with get_stream(output_file, 'w') as outfile:
            outfile.write("".join(text))
