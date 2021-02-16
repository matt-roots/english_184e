from pathlib import Path

kFileName = Path('hunger_games.txt')

def read_file(path):
    with open(path, 'r') as f:
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

def main():
    text = read_file(kFileName)
    print(text[:250])
    lines = read_lines(kFileName)
    print(lines[:10])
    cleaner_lines = loop_lines(kFileName)
    print(*cleaner_lines[:10], sep='\n')


if __name__ == '__main__':
    main()