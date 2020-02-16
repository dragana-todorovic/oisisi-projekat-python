# -*- coding: utf-8 -*-
def bfs(g, s, discovered):
    level = [s]  # prvi nivo uključuje samo s
    while len(level) > 0:
        next_level = []  # priprema za skupljanje novih čvorova
        for u in level:
            for e in g.incident_edges(u):  # za svaki odlazni čvor iz u
                v = e.opposite(u)
                if v not in discovered:  # v je neposjećen čvor
                    discovered[v] = e  # e je ivica preko koje je otkriven čvor v
                    next_level.append(v)  # v će biti razmotreno u sledećem prolazu
        level = next_level  # mijenjamo oznaku 'next' sljedećeg nivoa da postane trenutni


def bfs_complete(g):
    forest = {}
    for u in g.vertices():
        if u not in forest:
            forest[u] = None  # u će biti koren stabla
            bfs(g, u, forest)
    return forest
