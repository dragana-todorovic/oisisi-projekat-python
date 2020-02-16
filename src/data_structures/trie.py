class TrieNode:

    def __init__(self):
        self.children = {}
        self.terminating = False
        self.counter = 0
        self.indexes = {}


class Trie:

    def __init__(self):
        self.root = TrieNode()

    @staticmethod
    def get_index(ch):
        return ord(ch)

    def insert(self, word, file_path, index_in_file):

        root = self.root
        len1 = len(word)
        word = word.lower()

        for i in range(len1):
            index = self.get_index(word[i])
            if index not in root.children:
                root.children[index] = TrieNode()
            root = root.children.get(index)
        if file_path not in root.indexes.keys():
            root.indexes[file_path] = []
        root.indexes[file_path].append(index_in_file)
        root.word = word
        root.counter += 1

        root.terminating = True

    def search(self, word):
        word = word.lower()
        root = self.root
        len1 = len(word)

        for i in range(0, len1):
            index = self.get_index(word[i])
            if not root:
                return None
            root = root.children.get(index)

        if root and root.terminating:
            return root
        else:
            return None
