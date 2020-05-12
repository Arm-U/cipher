import argparse
import sys


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
