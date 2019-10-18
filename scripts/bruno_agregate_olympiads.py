import sys
import pandas as pd
from collections import Counter

tab = pd.read_csv("/home/administrator/Downloads/final_olimpiades.csv")

print(tab.columns)

print(tab.shape)
tab = tab[tab.School != ""]

counter = Counter()

for _, row in tab.iterrows():
    k = row["School"], row["Year"]
    counter[k] += 1

tab = {"school": [], "year": [], "cnt_olympiad_entries": []}
for (school, year), cnt in counter.items():
    tab["school"].append(school)
    tab["year"].append(year.split("_")[0])
    tab["cnt_olympiad_entries"].append(cnt)

tab = pd.DataFrame(tab)
tab.to_csv("/home/administrator/repos/edufuture/data/olympiads_agregated.csv", index=False)