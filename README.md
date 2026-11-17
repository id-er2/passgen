# passgen

A local command-line password and passphrase generator. Uses Python's `secrets` module and has no third-party dependencies or network code.

## Run

Python 3.8 or newer. Download this repository and keep `passgen.py` and `wordlists.py` in the same directory. No installation is needed.

```sh
python passgen.py password
python passgen.py password --length 28 --count 3
python passgen.py password --no-symbols
python passgen.py phrase
python passgen.py phrase --language ar
python passgen.py phrase --words 17 --separator " "
python passgen.py --help
```

On systems where `python` is not Python 3, use `python3`. Use a UTF-8 terminal for Arabic output.

Each result is printed on its own line. There is no automatic clipboard copy, file output, history, or telemetry in the program. Your terminal, shell session recorder, operating system, or clipboard manager can still retain what you display or copy. Do not generate real credentials in a shared terminal or post screenshots of them.

## Passwords

The default is 20 characters, with at least one lowercase letter, uppercase letter, digit, and symbol. `--no-symbols` keeps the first three groups. Length is limited to 12-4096 characters; `--count` accepts 1-100.

Each character is chosen with `secrets.choice`. If a candidate is missing an enabled character group, the whole candidate is rejected and generated again. The accepted strings are uniformly sampled from the strings satisfying those rules, rather than placing required characters in predictable positions.

The symbol alphabet is defined in `passgen.py`. It leaves out spaces, quotes, backslashes, and backticks for easier copying. Some services have different rules. Check the service before choosing a length or character set.

## Passphrases

The default is 12 independently chosen words joined by hyphens. English and Arabic lists each contain 211 distinct words. The Arabic list uses ordinary words for food, plants, nature, and household objects, without vowel marks or presentation-form characters. The lists are independently curated, not a translation table or an external dictionary dump.

```sh
python passgen.py phrase --language en --words 12
python passgen.py phrase --language ar --words 12
```

Words are chosen **with replacement**. A repeated word is possible and should not be manually removed. Supported separators are a hyphen, dot, underscore, or single space. Word count is limited to 8-64.

For either unchanged list, the random word choices provide:

| Words | Bits from word choices |
| --- | --- |
| 8 | 61.8 |
| 12 (default) | 92.7 |
| 17 | 131.3 |

The formula is `word_count * log2(list_size)`. This assumes independent uniform choices from the original duplicate-free list, no edits to the phrase, and an attacker who knows the list and settings. A fixed separator adds no entropy. This is not a crack-time prediction or a guarantee of account safety. Fewer than 80 bits prints a warning to stderr. The wordlists are intentionally small, so use more words than you would with a much larger list.

Arabic passphrases need a service that accepts Arabic Unicode text. Some services impose short maximum lengths, normalize characters, or reject non-ASCII input. A phrase of 12 or 17 words is long; use a random-character password when a service cannot accept it. Do not shorten a phrase by removing random words or substituting a personal sentence.

## Tests

```sh
python -m unittest -v
```

33 tests cover length and option limits, required character groups, whole-candidate rejection, word membership, repeated words, entropy arithmetic, CLI errors and warnings, and wordlist uniqueness, size, normalization, and scripts. Broad frequency and collision smoke tests run against the actual random source. They can catch gross mistakes but do not prove cryptographic security. There is no seed option; deterministic tests mock `secrets.choice` only inside the test suite.

## Limits

This tool generates strings. It does not store or manage passwords, check breaches, contact services, or protect an already-compromised device. It has not had an independent security audit. Use a trusted password manager to save a different password for every account, and turn on multi-factor authentication where available. Do not use a generated example from a README, screenshot, or chat as a real password.

## License

MIT. See [LICENSE](LICENSE).
