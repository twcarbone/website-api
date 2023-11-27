import argparse
import pathlib

from api import create_app
from api.models.grocery import ShopriteReceiptParser


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to receipt file or directory", metavar="path", type=pathlib.Path)
    args = parser.parse_args()
    if not args.path.exists():
        parser.error(f"path {args.path} is invalid")
    return args


def main():
    args = parse_args()

    with create_app().app_context():
        ShopriteReceiptParser.parse(args.path)


if __name__ == "__main__":
    main()
