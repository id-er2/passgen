"""Run with python -m unittest -v. No external services or packages needed."""

import ast
from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
import io
import math
from pathlib import Path
import re
import string
import unittest
import unicodedata
from unittest.mock import patch

import passgen
from wordlists import WORDLISTS


class PasswordTests(unittest.TestCase):
    def test_default_length(self):
        self.assertEqual(len(passgen.generate_password()), 20)

    def test_lengths(self):
        for length in (12, 13, 64, 4096):
            with self.subTest(length=length):
                self.assertEqual(len(passgen.generate_password(length)), length)

    def test_all_groups(self):
        for _ in range(100):
            password = passgen.generate_password(12)
            self.assertTrue(all(any(c in group for c in password) for group in passgen.GROUPS))

    def test_alphabet(self):
        self.assertLessEqual(set(passgen.generate_password(4096)), set(''.join(passgen.GROUPS)))

    def test_no_symbols(self):
        password = passgen.generate_password(4096, symbols=False)
        self.assertLessEqual(set(password), set(string.ascii_letters + string.digits))
        self.assertTrue(all(any(c in group for c in password) for group in passgen.GROUPS[:3]))

    def test_invalid_lengths(self):
        for value in (-1, 0, 4, 11, 4097, '20', 20.0, True, None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                passgen.generate_password(value)

    def test_invalid_symbol_flag(self):
        for flag in (1, None, 'yes'):
            with self.assertRaises(ValueError):
                passgen.generate_password(symbols=flag)

    def test_whole_candidate_rejection(self):
        candidates = list('a' * 12 + 'aA1!' * 3)
        with patch('passgen.secrets.choice', side_effect=candidates) as choice:
            self.assertEqual(passgen.generate_password(12), 'aA1!' * 3)
            self.assertEqual(choice.call_count, 24)

    def test_random_sample_uniqueness(self):
        self.assertEqual(len({passgen.generate_password() for _ in range(500)}), 500)

    def test_character_distribution_sanity(self):
        # Broad, low-flake smoke test. It does not prove cryptographic security.
        counts = Counter(''.join(passgen.generate_password(4096) for _ in range(8)))
        alphabet = ''.join(passgen.GROUPS)
        expected = 32768 / len(alphabet)
        self.assertEqual(set(counts), set(alphabet))
        self.assertTrue(all(expected * .5 < counts[c] < expected * 1.5 for c in alphabet))


class PhraseTests(unittest.TestCase):
    def test_default_words(self):
        self.assertEqual(len(passgen.generate_phrase().split('-')), 12)

    def test_languages(self):
        for language, wordlist in WORDLISTS.items():
            with self.subTest(language=language):
                self.assertLessEqual(set(passgen.generate_phrase(64, language).split('-')), set(wordlist))

    def test_separators(self):
        for separator in passgen.SEPARATORS:
            self.assertEqual(len(passgen.generate_phrase(12, 'ar', separator).split(separator)), 12)

    def test_repetition_is_allowed(self):
        with patch('passgen.secrets.choice', return_value=WORDLISTS['ar'][0]) as choice:
            self.assertEqual(passgen.generate_phrase(8, 'ar'), '-'.join([WORDLISTS['ar'][0]] * 8))
            self.assertEqual(choice.call_count, 8)
            self.assertEqual(choice.call_args.args[0], WORDLISTS['ar'])

    def test_invalid_word_counts(self):
        for words in (0, 7, 65, '12', 12.0, True, None):
            with self.subTest(words=words), self.assertRaises(ValueError):
                passgen.generate_phrase(words)

    def test_invalid_languages(self):
        for language in ('fa', '', None, 'EN'):
            with self.assertRaises(ValueError):
                passgen.generate_phrase(language=language)

    def test_invalid_separators(self):
        for separator in ('', '\n', '\x1b', 'xx', None):
            with self.assertRaises(ValueError):
                passgen.generate_phrase(separator=separator)

    def test_entropy(self):
        for language in WORDLISTS:
            self.assertAlmostEqual(passgen.phrase_entropy(12, language), 12 * math.log2(211))
            self.assertGreater(passgen.phrase_entropy(12, language), 90)
            self.assertLess(passgen.phrase_entropy(8, language), 80)

    def test_word_distribution_sanity(self):
        for language, wordlist in WORDLISTS.items():
            counts = Counter()
            for _ in range(500):
                counts.update(passgen.generate_phrase(64, language).split('-'))
            expected = 32000 / len(wordlist)
            self.assertEqual(set(counts), set(wordlist))
            self.assertTrue(all(expected * .4 < counts[w] < expected * 1.6 for w in wordlist))


class WordlistTests(unittest.TestCase):
    def test_sizes(self):
        self.assertEqual({k: len(v) for k, v in WORDLISTS.items()}, {'en': 211, 'ar': 211})

    def test_unique(self):
        for words in WORDLISTS.values():
            self.assertEqual(len(words), len(set(words)))

    def test_nfc(self):
        for words in WORDLISTS.values():
            self.assertTrue(all(w == unicodedata.normalize('NFC', w) for w in words))

    def test_english_letters(self):
        self.assertTrue(all(re.fullmatch('[a-z]+', w) for w in WORDLISTS['en']))

    def test_arabic_letters(self):
        self.assertTrue(all(re.fullmatch('[\u0621-\u063a\u0641-\u064a]+', w) for w in WORDLISTS['ar']))

    def test_no_separators_or_controls(self):
        for words in WORDLISTS.values():
            self.assertTrue(all(w and w.isalpha() and not any(c in w for c in passgen.SEPARATORS) for w in words))

    def test_imports_are_local_or_standard_library(self):
        allowed = {'argparse', 'math', 'secrets', 'string', 'sys', 'wordlists'}
        for filename in ('passgen.py', 'wordlists.py'):
            tree = ast.parse(Path(__file__).with_name(filename).read_text(encoding='utf-8'))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    self.assertTrue(all(a.name in allowed for a in node.names))
                elif isinstance(node, ast.ImportFrom):
                    self.assertIn(node.module, allowed)


class CliTests(unittest.TestCase):
    def run_cli(self, arguments):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            result = passgen.main(arguments)
        return result, out.getvalue(), err.getvalue()

    def test_password(self):
        code, out, err = self.run_cli(['password'])
        self.assertEqual(code, 0)
        self.assertEqual(len(out.strip()), 20)
        self.assertEqual(err, '')

    def test_count(self):
        _, out, _ = self.run_cli(['password', '--count', '4', '--no-symbols'])
        self.assertEqual(len(out.splitlines()), 4)
        self.assertTrue(all(line.isalnum() for line in out.splitlines()))

    def test_arabic(self):
        _, out, err = self.run_cli(['phrase', '--language', 'ar'])
        self.assertEqual(len(out.strip().split('-')), 12)
        self.assertEqual(err, '')

    def test_short_phrase_warning(self):
        _, out, err = self.run_cli(['phrase', '--words', '8'])
        self.assertEqual(len(out.strip().split('-')), 8)
        self.assertIn('80 bits', err)

    def test_space_separator(self):
        _, out, _ = self.run_cli(['phrase', '--separator', ' '])
        self.assertEqual(len(out.strip().split(' ')), 12)

    def test_bad_arguments_no_output(self):
        for args in ([], ['password', '--count', '0'], ['password', '--count', '101'],
                     ['password', '--length', '11'], ['phrase', '--words', '7'],
                     ['phrase', '--language', 'fa'], ['phrase', '--separator', '\n'],
                     ['password', '--length', 'x'], ['missing']):
            out, err = io.StringIO(), io.StringIO()
            with self.subTest(args=args), redirect_stdout(out), redirect_stderr(err):
                with self.assertRaises(SystemExit) as exit_status:
                    passgen.main(args)
                self.assertEqual(exit_status.exception.code, 2)
                self.assertEqual(out.getvalue(), '')

    def test_help(self):
        with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as result:
            passgen.main(['--help'])
        self.assertEqual(result.exception.code, 0)


if __name__ == '__main__':
    unittest.main()
