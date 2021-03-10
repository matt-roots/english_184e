from pathlib import Path
import csv
import os

kCorpusDir = Path('./corpus/')
kCountsDir = Path('./counts/')
def generate_outpath(path):
    """
    path represents the name of a file in ./corpus (for example, ./corpus/file1.txt). return a string representing a
    corresponding path to a csv in the ./counts directory with the same name (e.g., ./counts/file1.csv)
    """
    p = Path(path)
    file_p = path.name
    file_p.with_suffix('.csv')
    full_path = kCountsDir / p
    return str(full_path)

def write_lists(path, list1, list2):
    """
    list1 and list2 represent the keys and values from a word counts dictionary,
    and are guaranteed to be the same length. Your function should open path for writing,
    then write a csv consisting of rows consisting of (word, count), where word comes from
    from list1 and count from list2. The first row contains the first item from each list,
    the second row the second item from each list, etc. Hint: you may want to use a range-based for loop.
    """
    with open(path, 'w', encoding="UTF-8") as f:
        writer = csv.writer(f, dialect=csv.unix_dialect)
        # header_tuple = ('word', 'count')
        # writer.writerow(header_tuple)
        header_list = ['word', 'count']
        writer.writerow(header_list)
        for i in range(len(list1)):
            row = [list1[i], list2[i]]
            writer.writerow(row)

def shouty_list(ls):
    """
    >>> shouty_list("here are some words".split())
    ['HERE', 'ARE', 'SOME', 'WORDS']
    """
    for i in range(len(ls)):
        ls[i] = ls[i].upper()
    return ls

def convert_to_freqs(counts_dict):
    """
    takes the supplied dictionary mapping words to counts and normalizes them by dividing each count by the total
    number of words referenced by the dictionary, then returns the modified dictionary.
    Hint: look at the specification for homework 7 for a discussion of how to get the total
    number of words from a counts dictionary
    >>> convert_to_freqs({'the': 1208, 'and': 704})
    {'the': 0.6317991631799164, 'and': 0.3682008368200837}
    """
    length = sum(counts_dict.values())
    for key in counts_dict:
        counts_dict[key] = counts_dict[key] / length
    return counts_dict


def count_file_exts(path):
    """
    assuming that path is a pathlib path object that represents a directory containing zero or more files,
    counts the number of times each file extension appears in the names of those files and returns a dictionary
    that maps the file extensions (with or without the preceding '.', as you prefer) to the number of appearances
    of each. e.g. {".csv": 2, ".tex": 1, ".txt": 14}. Hint: iterate over all the items in the directory.
    """
    counts = {}
    for file_path in path.iterdir():
        suffix = Path(file_path).suffix
        if suffix not in counts:
            counts[suffix] = 0
        counts[suffix] += 1
    print(counts)



if __name__ == '__main__':
    import doctest
    doctest.testmod()
    cwd = Path('c:/')
    count_file_exts(cwd)
