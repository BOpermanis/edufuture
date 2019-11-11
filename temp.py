import pickle
import sys
from textdistance import lcsseq
import numpy as np
from pprint import pprint

with open("/home/administrator/repos/edufuture/data/list_schools_dont_match.pickle", "rb") as conn:
    list_schools_dont_match = pickle.load(conn)


def similarity(v1, v2):
    lc = lcsseq(v1, v2)
    return len(lc) / (len(v1) + len(v2) - len(lc))
    # return len(lc)


for d, d1 in list_schools_dont_match:
    print(len(d), len(d1))
    if len(d) < len(d1):
        l = sorted(list(d)) # isaakaa sekvence
        l1 = sorted(list(d1))
    else:
        l1 = sorted(list(d))  # isaakaa sekvence
        l = sorted(list(d1))

    simmat = np.zeros((len(l), len(l1)))
    for i, v in enumerate(l):
        for i1, v1 in enumerate(l1):
            simmat[i, i1] = similarity(v, v1)

    matches = []
    for i, row in enumerate(simmat):
        if np.max(row) > 0.8:#* len(l[i]):
            i0 = np.argmax(row)
            matches.append((l[i], l1[i0]))
            # print(row[i0])
            # print(l[i])
            # print(l1[i0])
            # sys.exit()
    print("-------------------------")
    pprint(matches)
