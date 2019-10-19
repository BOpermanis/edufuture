import sys
import pandas as pd
from pprint import pprint
import numpy as np
from glob import glob
from re import findall

# tab = pd.read_csv("/home/administrator/repos/edufuture/data/Master_table.csv", sep="|")
tab = pd.read_excel("/home/administrator/repos/edufuture/data/Master_table.xlsx")

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

def normalize_shool_name(name):
    return name.replace(" ", "").lower().replace(".", "").replace(",", "")

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


set_eksamenu_prieksmeti = set()
years = set()
school_names = set()
for f in glob("/home/administrator/Downloads/Exam results/*.csv"):
    print(f)
    tab1 = pd.read_csv(f)
    tab1.fillna(value="", inplace=True)
    print(tab1.shape)
    year = int(findall(r'[0-9]*_([0-9]*).csv', f)[0])
    school_name = "Izglītības iestāde" if "Izglītības iestāde" in tab1.columns else "Skola"
    school_name = "Izglītībasiestāde" if school_name not in tab1.columns else school_name
    school_name = "IzglītībasIestāde" if school_name not in tab1.columns else school_name
    school_name = "Nosaukums" if school_name not in tab1.columns else school_name

    tab1[school_name] = tab1[school_name].apply(normalize_shool_name)
    tab1.fillna(value="", inplace=True)
    s = set(list(tab1[school_name]))
    s1 = set(list(tab["School_Name"]))
    print(len(s.intersection(s1)) / len(s))
    # sys.exit()
    dict_schooldata_to_ol = {}
    # print(year)
    # print(tab['Year'])
    # sys.exit()
    for _, row in tab1.iterrows():
        set_eksamenu_prieksmeti.add(row['Priekšmets'])
        years.add(int(year))
        school_names.add(row[school_name])
        dict_schooldata_to_ol[(row[school_name], int(year), row['Priekšmets'])] = row["Kopvērtējums"]
    # for exam in set_eksamenu_prieksmeti:
    #     column_name = "{}_{}"
    # print(len(dict_schooldata_to_ol))
    # # print(tab1)
    # sys.exit()

# pprint(list(np.unique(tab['School_Name'])))

s_School_Name = set(list(tab['School_Name']))
s_Year = set(list(tab['Year']))

print(len(s_School_Name.intersection(school_names)))
print(len(s_Year.intersection(years)))
# print(s_Year)
# print(years)
print(set_eksamenu_prieksmeti)
# sys.exit()

print(tab.columns)
# for exam in set_eksamenu_prieksmeti:
#
#     tab[exam] = tab.apply(lambda row: dict_schooldata_to_ol.get((row["School_Name"], int(row["Year"]), exam), -1),axis=1)
#     print(exam, tab[tab[exam]!=-1].shape[0] / tab.shape[0])

tab.to_csv("/home/administrator/repos/edufuture/data/modelling_table.csv", sep="|")
print(tab.shape)