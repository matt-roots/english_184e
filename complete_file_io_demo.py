"""
Completed file i/o demo. If you want to use this code, you'll need to create corpus and counts directories in the
directory where you run it.
"""


import csv
from pathlib import Path

kFileName = Path('hunger_games.txt')
kOutPath = Path('hunger_counts.csv')
kCorpusDir = Path('./corpus')

def read_file(path):
    with open(path, 'r', encoding="UTF-8") as f:
        text = f.read()
        return text

def read_lines(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        return lines

def loop_lines(path):
    with open(path, 'r') as f:
        lines = []
        for line in f:
            if line != '\n':
                lines.append(line)
        return lines

def write_counts(path, counts):
    with open(path, 'w', encoding="UTF-8") as f:
        writer = csv.writer(f, dialect=csv.unix_dialect)
        writer.writerow(['word', 'count'])
        for count in counts.items():
            writer.writerow(count)


def sort_counts(counts) -> list:
    """
    Takes in a dictionary of counts, and returns a sorted list of tuples containing the words and their counts. We won't
    cover how this works in class, but it's essentially a compact version of looping over the dictionary to make all the
    word-count pairs and put them into the list, and then sorting the list by the second item in each of those pairs
    (the count)
    """
    return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)


def count_all_words(text) -> dict:  # the equal sign means the parameter gets this value by "default"
    """
    >>> count_all_words("Once, me father Jeb gave me some advice.", dict_filter=False)
    {'once': 1, 'me': 2, 'father': 1, 'jeb': 1, 'gave': 1, 'some': 1, 'advice': 1}
    >>> count_all_words("Once, me father Jeb gave me some advice.", dict_filter=True)
    {'once': 1, 'me': 2, 'father': 1, 'gave': 1, 'some': 1, 'advice': 1}
    """
    counts = {}
    words = text.split()
    for word in words:
        word = word.lower().strip(',.:;?!\'\"')
        if word not in counts:
            counts[word] = 0
        counts[word] += 1
    return counts


def main():
    # hunger_counts: counting files in a single text file
    text = read_file(kFileName)
    counts = count_all_words(text)
    write_counts(kOutPath, counts)

    # corpus counts: counting all files in a directory
    for path in kCorpusDir.iterdir():
        print(f'Generating counts form {path}')
        text = read_file(path)
        counts = count_all_words(text)
        outfile = Path('./counts/' + path.name).with_suffix('.csv')
        write_counts(outfile, counts)
        print(f'Wrote counts to {outfile}')
    return 0


if __name__ == '__main__':
    main()
