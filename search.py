import csv
import load_data

ALPHABET, SEPARATION, RESERVED_WORDS = load_data.load()


def parsing(path):
    with open(path, 'r') as f:
        content = f.read().lower()

        lines = content.split('\n')

        comments = []
        identifiers = {}
        errors = []
        constants = {}

        big_comment = ""
        can_be_big_comment = False
        can_be_end_comment = False

        for number_line, line in enumerate(lines):
            characters = list(line)

            lex = ""

            can_be_constant = False
            ignore_error = False
            can_be_comment = False

            for key, character in enumerate(characters):

                if can_be_big_comment:
                    if character == "/" and can_be_end_comment:
                        comments.append(big_comment)
                        add_to_hash_map(SEPARATION, "/")
                        can_be_end_comment = can_be_big_comment = False
                        big_comment = ""
                        continue
                    if character == "*":
                        can_be_end_comment = True
                        add_to_hash_map(SEPARATION, "*")
                        continue
                    can_be_end_comment = False
                    big_comment += character
                    continue

                if can_be_constant:
                    if character == "'":
                        add_to_hash_map(constants, lex)
                        lex = ""
                        add_to_hash_map(SEPARATION, character)
                        can_be_constant = False
                    else:
                        lex += character
                    continue

                if character in ALPHABET:
                    lex += character
                else:

                    try:
                        add_to_hash_map(constants, int(character))
                        ignore_error = True
                    except:
                        pass

                    if character == "'":
                        can_be_constant = True

                    if not (character in SEPARATION or character in RESERVED_WORDS) and not ignore_error:
                        if len(lex) > 0:
                            errors.append((number_line, lex + character))
                        else:
                            errors.append((number_line, character))
                        break

                    if len(lex) > 0:
                        if lex in RESERVED_WORDS:
                            add_to_hash_map(RESERVED_WORDS, lex)
                        else:
                            add_to_hash_map(identifiers, lex)
                        lex = ""

                    if character == '/':
                        if can_be_comment:
                            comment = ''.join(characters[(key + 1):])
                            comments.append(comment.strip())
                            add_to_hash_map(SEPARATION, '/')
                            break
                        else:
                            can_be_comment = True

                    if character == '*' and can_be_comment:
                        can_be_big_comment = True
                        add_to_hash_map(SEPARATION, "*")
                        continue

                    if character in SEPARATION:
                        add_to_hash_map(SEPARATION, character)

                    ignore_error = False

        print(errors)

        save_dictionary_to_csv('identifiers.csv', identifiers)
        save_dictionary_to_csv('constants.csv', constants)
        save_dictionary_to_csv('separations.csv', SEPARATION)
        save_dictionary_to_csv('reserved_words.csv', RESERVED_WORDS)
        save_list_to_csv('comments.csv', comments)
        save_list_to_csv('errors.csv', errors)


def save_dictionary_to_csv(filename, dictionary):
    with open(filename, 'w', newline='') as csvfile:
        w = csv.DictWriter(csvfile, dictionary.keys())
        w.writeheader()
        w.writerow(dictionary)


def save_list_to_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(x for x in data)


def save_error_to_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for line, value in data:
            writer.writerow(line, value)


def add_to_hash_map(hash_map, value):
    if value in hash_map:
        hash_map[value] += 1
    else:
        hash_map[value] = 1


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default="file.txt")
    namespace = parser.parse_args()

    parsing(namespace.file)
