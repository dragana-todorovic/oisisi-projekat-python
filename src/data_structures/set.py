class Set:

    def __init__(self):
        self.d = {}

    def do_and(self, d1, d2):
        keys = []
        self.d = {}
        for k1 in d1:
            if k1 in d2.keys():
                keys.append(k1)
        for k in keys:
            grade = 0.5 * d1[k][0] + 0.5 * d2[k][0]
            for index in d2[k]:
                d1[k].append(index)
            self.d[k] = [grade, d1[k][1] + d2[k][1]]
        return self.d

    def do_or(self, d1, d2):
        keys = []
        self.d = {}
        for k1 in d1.keys():
            keys.append(k1)
        for k2 in d2.keys():
            if k2 not in keys:
                keys.append(k2)
        for k in keys:
            grade = 0
            if k in d1.keys() and k in d2.keys():
                grade += 0.5 * (d1[k][0] + d2[k][0])
                for index in d2[k]:
                    d1[k].append(index)
                self.d[k] = [grade, d1[k][1] + d2[k][1]]
            elif k in d1.keys():
                self.d[k] = [d1[k][0], d1[k][1]]
            else:
                self.d[k] = [d2[k][0], d2[k][1]]
        return self.d

    def do_not(self, d1, d2):
        keys = []
        self.d = {}
        for k1 in d1.keys():
            keys.append(k1)
        for k2 in d2.keys():
            if k2 in keys:
                keys.remove(k2)
        for k in keys:
            grade = d1[k][0]
            self.d[k] = [d1[k][0], d1[k][1]]
        return self.d
