import argparse

import api

import config


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        dest="debug",
        help="Enable debug mode",
    )
    parser.add_argument(
        "--config",
        choices=["Dev", "Test", "Prod"],
        default="Prod",
        dest="config",
        help="Load configuration class (Dev, Test, Prod).",
        metavar="STR",
    )
    parser.add_argument(
        "--port",
        default=5000,
        dest="port",
        help="Port to bind to.",
        metavar="INT",
        type=int,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    app = api.create_app(env=args.config)
    app.run()
