from src.data_structures.bfs import bfs_complete
from src.data_structures.graph import Graph
from src.data_structures.set import Set
from src.data_structures.trie import Trie, TrieNode
from src.file_walk import walk_recursively
from src.parser import Parser

g = Graph()
p = Parser()
t = Trie()
s = Set()
OKBLUE = '\033[94m'
ENDC = '\033[0m'
FAIL = '\033[91m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'


def create_trie(words_in_file, path_to_file):
    new_trie = Trie()
    for j in range(len(words_in_file)):
        new_trie.insert(words_in_file[j], path_to_file, j)
    return new_trie


def generate_trie():
    path = input("Unesi putanju:")
    if path.__contains__(".html"):
        print("Putanja nije odgovarajuca")
        path = input("Unesi putanju: ")
    files = walk_recursively(path)
    if not files:
        print('Nema html dokumenata u direktorijumu')
        return
    inserted = []
    for file_path in files:
        try:
            links, words = p.parse(file_path)

            u = g.insert_vertex({'path': file_path,
                                 'words': words,
                                 'trie': create_trie(words, file_path)})
            for index in range(len(words)):
                t.insert(words[index], file_path, index)

            for link in links:
                v = g.get_vertex(link)
                if v is None:
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


def single_search(word):
    dic = {}
    for k, v in forest.items():
        vertex = k
        page = vertex.element()

        if page["path"] in do_search(word).indexes.keys():
            grade = 0
            reference_num = g.degree(vertex, False)
            other_count = 0
            if v is not None:
                other_page = v.endpoints()[1].element()
                other_node = other_page["trie"].search(word)
                if other_node is not None:
                    other_count = other_node.counter
            grade += 0.5 * reference_num
            grade += 0.3 * other_count
            node = page["trie"].search(word)
            if node is not None:
                grade += 0.2 * node.counter
                dic[page["path"]] = [grade, node.counter]

    return dic


def sort_dict(dictionary):
    items = list(dictionary.items())
    merge_sort(items)
    return dict(items)


def merge_sort(dic_items):

    if len(dic_items) > 1:
        mid = len(dic_items) // 2
        left = dic_items[0:mid]

        right = dic_items[mid:len(dic_items)]
        merge_sort(left)
        merge_sort(right)

        m = 0
        j = 0
        k = 0
        while m < len(left) and j < len(right):
            if left[m][1][0] > right[j][1][0]:
                dic_items[k] = left[m]
                m = m + 1
            else:
                dic_items[k] = right[j]
                j = j + 1
            k = k + 1

        while m < len(left):
            dic_items[k] = left[m]
            m = m + 1
            k = k + 1

        while j < len(right):
            dic_items[k] = right[j]
            j = j + 1
            k = k + 1


def paginaiton_print(sorted_dic):
    try:
        if not sorted_dic:
            print("Nema rezultata.")
            return
        pagination_num = int(input("Koliko rezultata zelite da prikazete? "))
        if pagination_num <= 0:
            print("Ne moze se prikazati 0 ili negatvan broj rezultata")
            return
        lista_printova = []
        for key in sorted_dic:
            path = key
            range_ = sorted_dic[key][0]
            count = sorted_dic[key][1]
            print_string = " Putanja do html stranice koja sadrzi rijec(rijeci) je: " + OKBLUE + path + ENDC + "\n"
            print_string += "Broj pojavljivanja rijeci u datoj stranici je: " + OKGREEN + str(count) + ENDC + "\n"
            print_string += "Rang date stranice je: " + FAIL + str(range_) + ENDC + "\n--------------------------"
            lista_printova.append(print_string)
        index = 0
        while index + pagination_num < len(lista_printova):
            for index2 in range(index, index + pagination_num):
                print(lista_printova[index2])
            choice = input("Korak [next/prev]: ")
            if choice.lower() == "next":
                index += pagination_num
            elif choice.lower() == "prev":
                if index - pagination_num < 0:
                    print("Prvo next pa prev")
                else:
                    index -= pagination_num
            else:
                return
        for ind in range(index, len(lista_printova)):
            print(lista_printova[ind])
    except ValueError:
        print(" Morate unijeti broj !\n")


if __name__ == '__main__':
    generate_trie()
    forest = bfs_complete(g)

    while True:
        search_input = input("Search: ")
        search_input = search_input.strip("\n")
        search_input = search_input.strip(" ")
        word_list = search_input.split(" ")
        is_empty_search = len(word_list) == 1 and word_list[0] == ''
        d = {}
        if is_empty_search:
            print("Nije validan unos")
            break
        elif len(word_list) == 1:
            search_result = do_search(word_list[0])
            d = single_search(word_list[0])
            dic = sort_dict(d)
            paginaiton_print(dic)
        else:
            has_operator = False
            for operator in ["AND", "OR", "NOT", "and", "or", "not"]:
                if operator in word_list:
                    has_operator = True
            if has_operator:
                for i in range(0, len(word_list)):
                    if word_list[1].upper() in ["AND", "OR", "NOT"]:
                        search_result1 = do_search(word_list[i - 1])
                        search_result2 = do_search(word_list[i + 1])
                        if search_result1 is not None and search_result2 is not None:
                            if word_list[i].upper() == 'AND':
                                d = s.do_and(single_search(word_list[i - 1]), single_search(word_list[i + 1]))
                                dic = sort_dict(d)
                                paginaiton_print(dic)
                                break
                            elif word_list[i].upper() == 'OR':
                                d = s.do_or(single_search(word_list[i - 1]), single_search(word_list[i + 1]))
                                dic = sort_dict(d)
                                paginaiton_print(dic)
                                break
                            elif word_list[i].upper() == 'NOT':
                                d = s.do_not(single_search(word_list[i - 1]), single_search(word_list[i + 1]))
                                dic = sort_dict(d)
                                paginaiton_print(dic)
                                break
                else:
                    print("Nije validan unos")
            else:
                d = None
                for i in range(0, len(word_list) - 1):
                    first_time = i == 0
                    if first_time:
                        d = single_search(word_list[i])
                    search_result2 = single_search(word_list[i + 1])
                    if d is not None and search_result2 is not None:
                        d.update(s.do_or(d, search_result2))
                        d = sort_dict(d)
                paginaiton_print(d)
