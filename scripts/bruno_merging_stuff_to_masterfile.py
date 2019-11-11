import sys
import pandas as pd
from pprint import pprint
import numpy as np
from glob import glob
from re import findall
from scipy.spatial import distance_matrix
import pickle

# tab = pd.read_excel("/home/administrator/repos/edufuture/data/Master_table_with population.xlsx")
tab = pd.read_excel("/home/administrator/repos/edufuture/data/Master_table_cleaned_2.xlsx")

dict_pupil_cnt = {}
for _, row in tab.iterrows():
    dict_pupil_cnt[(row["School_Name"], row["Year"])] = row["Number_of_students"]



tab = tab[tab.Year > 2009]

tab["student_diff"] = tab.apply(lambda row: row["Number_of_students"] - dict_pupil_cnt[(row["School_Name"], row["Year"] - 1)], axis=1)

# iedz skaits

tab["reg_iedz_skaits"] = tab.apply(lambda row: row['Republikas pilsētas populācija'] if row['Novada populācija'] == "--" else row['Novada populācija'], axis=1)

tab["Year"] = tab["Year"].apply(int)

# nearest school
tab.sort_values(by="Year", inplace=True)
dict_closest_distance = {}

for year, tab1 in tab.groupby("Year"):
    coords = np.stack([tab1['LAT'], tab1['LON']], axis=1)
    school_names = list(tab1['School_Name'])

    dists = distance_matrix(coords, coords)
    for i, name in enumerate(school_names):
        inds = np.argsort(dists[i, :])

        for i0 in inds:
            if dists[i, i0] > 0:
                dict_closest_distance[(name, year)] = dists[i, i0]
                break

tab["dist_to_nierest"] = tab.apply(lambda row: dict_closest_distance[(row["School_Name"], row["Year"])], axis=1)

print(tab.columns)
tab.fillna(value="", inplace=True)
tab = tab[tab.Number_of_students > 0]

## dependant variable
set_shool_year_pairs = set()
for _, row in tab.iterrows():
    set_shool_year_pairs.add((row["School_Name"], row["Year"]))

tab = tab[tab.Year <= 2018]


def generate_Y(row):
    return (row["School_Name"], row["Year"] + 1) in set_shool_year_pairs


tab["Y"] = tab.apply(generate_Y, axis=1)

print(np.unique(tab["Y"], return_counts=True))

tab1 = pd.read_csv("/home/administrator/repos/edufuture/data/olimpiades_group_by.csv", sep=",")
tab1.fillna(value="", inplace=True)

print(tab.columns)
print(tab1.columns)
# print(tab1)
# sys.exit()

dict_normletter = { 'ā': 'a', 'č': 'c', 'ē': 'e', 'ģ': 'g', 'ī': 'i', 'ķ': 'k', 'ļ': 'l', 'ņ': 'n', 'š': 's', 'ū': 'u', 'ž': 'z'}

def normalize_shool_name(name):
    name = name.replace(" ", "").lower().replace(".", "").replace(",", "").replace('"', '')
    name = "".join(list(map(lambda letter: dict_normletter.get(letter, letter), name)))
    return name

tab['School_Name_original'] = tab['School_Name']
tab['School_Name'] = tab['School_Name'].apply(normalize_shool_name)
tab1['school'] = tab1['school'].apply(normalize_shool_name)

tab1['year'] = tab1['year'].apply(lambda x: int(x.split("_")[0]))
tab1['year'] += 1


nms = set(list(tab.School_Name))
nms1 = set(list(tab1.school))

print(len(nms))
print(len(nms1))
print(len(nms.intersection(nms1)))

# skolas kas nemačojas
pprint(nms1.difference(nms))

dict_schooldata_to_ol = {}
for _, row in tab1.iterrows():
    dict_schooldata_to_ol[(row["school"], row["year"])] = row["cnt_olympiad_entries"]

print(np.unique(tab1["year"]))
print(np.unique(tab["Year"]))
# pprint(dict_schooldata_to_ol)

tab["cnt_olympiad_entries"] = tab.apply(lambda row: dict_schooldata_to_ol.get((row["School_Name"], row["Year"]), 0), axis=1)

del tab1
set_eksamenu_prieksmeti = set()
dict_schooldata_to_ol = {}

list_schools_dont_match = []

for f in glob("/home/administrator/Downloads/Exam results/*.csv"):
    print(f)
    tab_exam = pd.read_csv(f)
    tab_exam.fillna(value="", inplace=True)
    # print(tab_exam.shape)
    year = int(findall(r'[0-9]*_([0-9]*).csv', f)[0])

    school_name = "Izglītības iestāde" if "Izglītības iestāde" in tab_exam.columns else "Skola"
    school_name = "Izglītībasiestāde" if school_name not in tab_exam.columns else school_name
    school_name = "IzglītībasIestāde" if school_name not in tab_exam.columns else school_name
    school_name = "Nosaukums" if school_name not in tab_exam.columns else school_name

    novads = "Novads"

    if novads not in tab_exam.columns:
        tab_exam[novads] = ""

    tab_exam[school_name] = tab_exam[school_name].apply(normalize_shool_name)
    tab_exam[school_name + "_1"] = tab_exam.apply(lambda row: normalize_shool_name(str(row[novads]) + ", " + row[school_name]), axis=1)
    tab_exam.fillna(value="", inplace=True)

    s = set(list(tab_exam[school_name]))
    s1 = set(list(tab["School_Name"]))
    print(len(s.intersection(s1)) / len(s))
    d = s.difference(s1)
    d1 = s1.difference(s)
    list_schools_dont_match.append((d, d1))

    for _, row in tab_exam.iterrows():
        r = row["Kopvērtējums"]
        if isinstance(r, str):
            r = float(r.replace("%",""))
        set_eksamenu_prieksmeti.add(row['Priekšmets'])
        dict_schooldata_to_ol[(row[school_name], int(year), row['Priekšmets'])] = r
        dict_schooldata_to_ol[(row[school_name] + "_1", int(year), row['Priekšmets'])] = r

for exam in set_eksamenu_prieksmeti:
    tab[exam] = tab.apply(lambda row: dict_schooldata_to_ol.get((row["School_Name"], int(row["Year"]), exam), -1),axis=1)
    print(exam, tab[tab[exam]!=-1].shape[0] / tab.shape[0])

tab.to_csv("/home/administrator/repos/edufuture/data/modelling_table.csv", sep="|")
print(tab.shape)

with open("/home/administrator/repos/edufuture/data/list_schools_dont_match.pickle", "wb") as conn:
    pickle.dump(list_schools_dont_match, conn)