#!/usr/bin/env python3
"""Generate passwords and passphrases locally using the OS random source."""

import argparse
import math
import secrets
import string
import sys

from wordlists import WORDLISTS

SYMBOLS = "!#$%&()*+,-./:;<=>?@[]^_{|}~"
GROUPS = (string.ascii_lowercase, string.ascii_uppercase, string.digits, SYMBOLS)
SEPARATORS = ("-", ".", "_", " ")


def _integer(value, name, minimum, maximum):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError("{} must be an integer from {} to {}".format(name, minimum, maximum))


def generate_password(length=20, symbols=True):
    """Uniformly sample strings conditioned on containing every enabled group."""
    _integer(length, "length", 12, 4096)
    if type(symbols) is not bool:
        raise ValueError("symbols must be a boolean")
    groups = GROUPS if symbols else GROUPS[:3]
    alphabet = "".join(groups)
    # Reject the entire candidate, not individual characters. This avoids
    # favoring positions or outputs when enforcing character-class rules.
    while True:
        candidate = "".join(secrets.choice(alphabet) for _ in range(length))
        if all(any(char in group for char in candidate) for group in groups):
            return candidate


def _phrase_list(language):
    if language not in WORDLISTS:
        raise ValueError("language must be en or ar")
    return WORDLISTS[language]


def phrase_entropy(words=12, language="en"):
    """Bits from independent uniform word choices, not a crack-time estimate."""
    _integer(words, "words", 8, 64)
    return words * math.log2(len(_phrase_list(language)))


def generate_phrase(words=12, language="en", separator="-"):
    """Choose with replacement: repeated words are allowed and intentional."""
    _integer(words, "words", 8, 64)
    wordlist = _phrase_list(language)
    if separator not in SEPARATORS:
        raise ValueError("separator must be a hyphen, dot, underscore, or space")
    return separator.join(secrets.choice(wordlist) for _ in range(words))


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    password = modes.add_parser("password", help="random characters (default: 20)")
    password.add_argument("--length", type=int, default=20)
    password.add_argument("--no-symbols", action="store_true")
    phrase = modes.add_parser("phrase", help="independent random words (default: 12)")
    phrase.add_argument("--words", type=int, default=12)
    phrase.add_argument("--language", choices=tuple(WORDLISTS), default="en")
    phrase.add_argument("--separator", choices=SEPARATORS, default="-")
    for mode in (password, phrase):
        mode.add_argument("--count", type=int, default=1)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        _integer(args.count, "count", 1, 100)
        if args.mode == "phrase":
            bits = phrase_entropy(args.words, args.language)
            if bits < 80:
                print("Warning: fewer than 80 bits from word choices; use more words.", file=sys.stderr)
            # Validate before any output, including the separator.
            if args.separator not in SEPARATORS:
                raise ValueError("invalid separator")
        else:
            _integer(args.length, "length", 12, 4096)
        for _ in range(args.count):
            if args.mode == "phrase":
                print(generate_phrase(args.words, args.language, args.separator))
            else:
                print(generate_password(args.length, not args.no_symbols))
    except ValueError as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        raise SystemExit(1)
    except KeyboardInterrupt:
        raise SystemExit(130)
