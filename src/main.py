from src.parser import Parser
from src.data_structures.trie import Trie
from src.file_walk import walk_recursively

p = Parser()
t = Trie()


def generate_trie():
    path = input("Unesi putanju:")
    files = walk_recursively(path)
    for file_path in files:
        try:
            links, words = p.parse(file_path)
            print(words)
            for index in range(len(words)):
                t.insert(words[index], file_path, index)
        except Exception as e:
            print(f"Parsing error ${e}.")


if __name__ == '__main__':
    generate_trie()
