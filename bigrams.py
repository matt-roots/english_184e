import csv
from pathlib import Path
from typing import Optional, Any


kCorpusDir = Path('E:\dh\CHICAGO_CORPUS\CHICAGO_NOVEL_CORPUS')
kStopWords = Path('./nltk_english_stopwords.txt')
kCountsPath = Path('chicago_counts.csv')
kBigramPath = Path('chicago_bigrams.csv')
kCountsDir = Path('./counts/')
kBigramDir = Path('./bigrams/')



def read_stopwords() -> set:
    stopwords = set()
    with open(kStopWords) as f:
        for line in f.readlines():
            stopwords.add(line.strip())
    return stopwords


def sort_counts(counts) -> list:
    """
    Takes in a dictionary of counts, and returns a sorted list of tuples containing the words and their counts. We won't
    cover how this works in class, but it's essentially a compact version of looping over the dictionary to make all the
    word-count pairs and put them into the list, and then sorting the list by the second item in each of those pairs
    (the count)
    """
    return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)

def main():

    # count all the words in string
    corpus_counts = {}
    corpus_bigrams = {}
    corpus_len = 0
    count = 0

    for file in kCorpusDir.iterdir():
        # print(f'Reading {file.name}')
        if file.name.endswith(".txt"):
            try:
                counts_path = Path("./counts/" + file.name).with_suffix(".csv")
                with open(file, 'r', encoding="UTF-8") as f:
                    text = f.read()
                    counts, bigrams = count_words_and_bigrams(text, corpus_counts, corpus_bigrams)
                    for count in counts.values():
                        corpus_len += count
                    sorted_counts = sort_counts(counts)
                    sorted_bigrams = sort_counts(bigrams)
                counts_path = Path(kCountsDir + file.name).with_suffix(".csv")
                with open(counts_path, 'w', encoding="UTF-8") as f:
                    writer = csv.writer(f, dialect=csv.unix_dialect)
                    writer.writerow(['word', 'count'])
                    writer.writerows(sorted_counts)
                bigrams_path = Path(kCountsPath + file.name).with_suffix(".csv")
                with open(bigrams_path, 'w', encoding="UTF-8") as f:
                    writer = csv.writer(f, dialect=csv.unix_dialect)
                    writer.writerow(['bigram', 'count'])
                    writer.writerows(sorted_bigrams)
            except UnicodeError as e:
                print(f"OS / encoding error while reading file {file.name}")
                print(e)
            count += 1
            if count % 100 == 0:
                print(f'{count} files read so far')

    # norm corpus-level counts:
    for word in corpus_counts:
        corpus_counts[word] = corpus_counts[word] / corpus_len
    for bigram in corpus_bigrams:
        corpus_bigrams[bigram] = corpus_bigrams[bigram] / corpus_len

    # write counts dict to file
    sorted_counts = sort_counts(corpus_counts)
    with open(kCountsPath, 'w', encoding="UTF-8") as outfile:
        writer = csv.writer(outfile, dialect=csv.unix_dialect)
        writer.writerow(['word', 'count'])
        for count in sorted_counts:
            writer.writerow(count)

    # write bigrams to file
    sorted_bigrams = sort_counts(corpus_bigrams)
    with open(kBigramPath, 'w', encoding="UTF-8") as outfile:
        writer = csv.writer(outfile, dialect=csv.unix_dialect)
        writer.writerow(['bigram', 'count'])
        for bigram_count in sorted_bigrams:
            writer.writerow(bigram_count)

    return 0


if __name__ == '__main__':
    main()
