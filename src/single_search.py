def single_search(word, forest):
    dic = {}
    for k, v in forest.items():
        vertex = k
        page = vertex.element()
        node = page["trie"].search(word)
        if node is not None:
            dic[page["path"]] = [0, 0]
    return dic
