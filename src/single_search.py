from src.data_structures.graph import Graph
g = Graph()


def single_search(word, forest):
    dic = {}
    for k, v in forest.items():
        vertex = k
        page = vertex.element()
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
