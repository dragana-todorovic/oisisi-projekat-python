from src.parser import Parser
from src.data_structures.trie import Trie, TrieNode
from src.file_walk import walk_recursively
from src.data_structures.graph import Graph
from src.data_structures.bfs import bfs_complete

g = Graph()
p = Parser()
t = Trie()


def create_trie(words_in_file, path_to_file):
    new_trie = Trie()
    for j in range(len(words_in_file)):
        new_trie.insert(words_in_file[j], path_to_file, j)
    return new_trie


def generate_trie():
    path = input("Unesi putanju:")
    files = walk_recursively(path)
    for file_path in files:
        try:
            links, words = p.parse(file_path)

            u = g.insert_vertex({'path': file_path,
                                 'words': words,
                                 'trie': create_trie(words, file_path)})
            for index in range(len(words)):
                t.insert(words[index], file_path, index)

            for link in links:
                v = g.insert_vertex({'path': link,
                                     'words': words,
                                     'trie': create_trie(words, link)})
                g.insert_edge(u, v)
        except Exception as e:
            print(f"Parsing error ${e}.")


def find_page_in_forest(path, forest):
    for k, v in forest.items():
        page = k.element()
        if page is not None and page["path"] == path:
            return k.element()

def do_search(word):
    result = t.search(word)
    return result if result is not None else TrieNode()


if __name__ == '__main__':
    generate_trie()
    forest = bfs_complete(g)
    while True:
        search_input = input("Search: ")
        search_input = search_input.strip("\n")
        search_input = search_input.strip(" ")
        word_list = search_input.split(" ")
        is_empty_search = len(word_list) == 1 and word_list[0] == ''
        d = None
        if is_empty_search:
            print("Nije validan unos")
            break
        elif len(word_list) == 1:
            search_result = do_search(word_list[0])
            print(list(search_result.indexes.keys()))
