import string

ALPHABET = list(string.ascii_lowercase)
SEPARATION = [" ", ":", ";", "(", ")", "-", "+", "=", "/", "*", "'", "\"", "{", "}"]
RESERVED_WORDS = ["if", "else", "while", "for", "foreach", "switch", "function", "class"]


def load():
    dict_separation = {}
    for item in SEPARATION:
        dict_separation[item] = 0

    dict_reserved_words = {}
    for item in RESERVED_WORDS:
        dict_reserved_words[item] = 0

    return ALPHABET, dict_separation, dict_reserved_words
