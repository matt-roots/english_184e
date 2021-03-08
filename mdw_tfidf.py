import csv
from pathlib import Path
import math

kCorpusFreqs = Path('./chicago_freqs.csv')
kCorpusIDFs = Path('./mdw-tfidf/chicago_idfs.csv')
kCountsDir = Path('./counts')
kNovel = Path('./mdw-tfidf/austen_pride_and_prejudice.txt')
kStats = Path('./mdw-tfidf/austen_pride_and_prejudice_stats.csv')


def get_novel_freqs(path):
    """
    Reads a text file into a frequencies dictionary
    :param path:
    :return:
    """
    length = 0
    freqs = {}
    with open(path, 'r', encoding="UTF-8") as f:
        for word in f.read().split():
            length += 1
            word = word.lower().strip(',.:;?!\'\"“”()')
            if any(char in word for char in '/()-—_'):  # ignore words containing garbage
                continue
            else:
                if word not in freqs:
                    freqs[word] = 0
                freqs[word] += 1
    for word in freqs:
        freqs[word] = freqs[word] / length
    return freqs


def read_corpus_freqs(path) -> dict:
    """
    reads corpus frequencies from file kCorpusFreqs
    """
    freqs = {}
    with open(path, 'r', encoding="UTF-8") as f:
        reader = csv.DictReader(f)
        for line in reader:
            freq = float(line['freq'])
            word = line['word']
            freqs[word] = freq
    return freqs

def read_idfs(path):
    idfs = {}
    with open(path, 'r', encoding="UTF-8") as f:
        reader = csv.DictReader(f)
        for line in reader:
            idf = float(line['idf'])
            word = line['word']
            idfs[word] = idf
    return idfs


def get_idfs(path) -> dict:
    """
    Returns a dictionary of words mapped to the number of docs that contain them
    """
    idfs = {}
    doc_count = 0
    # get raw doc counts
    for file in path.iterdir():
        doc_count += 1
        with open(file, 'r', encoding="UTF-8") as f:
            reader = csv.reader(f)
            reader.__next__()
            for line in reader:
                if line[0] not in idfs:
                    idfs[line[0]] = 0
                idfs[line[0]] += 1
    for idf in idfs:
        idfs[idf] = math.log(doc_count / (idfs[idf]))
    return idfs


def make_stats(text_freqs, corpus_freqs, idfs):
    """
    Compiles frequency dictionaries into a list of lists of MDWs and tfidfs
    """
    rows = []
    for word in text_freqs:
        if word in corpus_freqs and word in idfs:
            rows.append([word, text_freqs[word], corpus_freqs[word],
                         text_freqs[word] / corpus_freqs[word], text_freqs[word] * idfs[word]])
    return rows


def main():
    # read corpus freqs from file
    corpus_freqs = read_corpus_freqs(kCorpusFreqs)

    novel_freqs = get_novel_freqs(kNovel)

    if kCorpusIDFs.exists():
        idfs = read_idfs(kCorpusIDFs)
    else:
        idfs = get_idfs(kCountsDir)
        with open(kCorpusIDFs, 'w', encoding="UTF-8") as f:
            fieldnames = ['word', 'idf']
            writer = csv.writer(f, dialect=csv.unix_dialect)
            writer.writerow(fieldnames)
            writer.writerows(list(idfs.items()))

    stats = make_stats(novel_freqs, corpus_freqs, idfs)
    stats = sorted(stats, key=lambda x: x[3], reverse=True)  # sort to get MDWs at top

    with open(kStats, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, dialect=csv.unix_dialect)
        writer.writerow(['word', 'text_freq', 'corpus_freq', 'distinctiveness', 'tf-idf'])
        writer.writerows(stats)
    return 0


if __name__ == '__main__':
    main()
