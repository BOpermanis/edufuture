import sys
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")


tab = pd.read_csv("/home/administrator/repos/edufuture/data/modelling_table.csv", sep="|")
print(np.unique(tab["Year"]))


x_names_cathegorical = ['Language']
x_names_nummerical = ["Number_of_students", "cnt_olympiad_entries", 'ANG9', 'MAT9', 'MAT12', 'LAT12', 'LAT9', 'ANG12', "dist_to_nierest", "reg_iedz_skaits", "student_diff", "yearlychange"]


def prepare_data(tab):
    X = tab[x_names_nummerical]
    for name in x_names_cathegorical:
        x1 = pd.get_dummies(tab[name])
        for cname in x1.columns:
            X[cname] = x1[cname]
    return X, tab["Y"]


# weights = list(range(10, 40))
# waccs = []
# for w in weights:
#     model = RandomForestClassifier(
#         criterion="entropy",
#         max_depth=5,
#         n_estimators=300,
#         n_jobs=4,
#         class_weight={0: w, 1: 1},
#         oob_score=True
#     )
#     # print(X)
#     X, Y = prepare_data(tab)
#     mask_train = tab.Year < 2018
#     mask_test = np.logical_not(mask_train)
#
#     model.fit(X[mask_train], Y[mask_train])
#     preds = model.predict(X[mask_test])
#     cm = confusion_matrix(Y[mask_test], preds)
#     wacc = np.average(np.diag(cm) / np.sum(cm, axis=1))
#     waccs.append(wacc)
#     print(w, wacc)
#
# w0 = weights[np.argmax(waccs)]
w0 = 28
print(w0)
# w0 = 15
model = RandomForestClassifier(
    random_state=0,
    criterion="entropy",
    max_depth=5,
    n_estimators=300,
    n_jobs=4,
    class_weight={0: w0, 1: 1},
    oob_score=True
)
# print(X)
X, Y = prepare_data(tab)
mask_train = tab.Year < 2018
mask_test = np.logical_not(mask_train)

# exam_vars = 'ANG9', 'MAT9', 'MAT12', 'LAT12', 'LAT9', 'ANG12'
# for v in exam_vars:
#     print(v, np.average(X[mask_test][v] !=-1))
# sys.exit()

model.fit(X[mask_train], Y[mask_train])
preds = model.predict(X[mask_test])
cm = confusion_matrix(Y[mask_test], preds)

# output = pd.DataFrame({
#     "school_name": tab[mask_test]["School_Name"],
#     "prob_survive": model.predict_proba(X[mask_test])
# })

tab["prob_survival"] = -1.0
tab["prob_survival"][mask_test] = model.predict_proba(X[mask_test])[:, 1]

plt.hist(tab["prob_survival"][mask_test])
plt.show()

tab.to_csv("/home/administrator/repos/edufuture/data/school_predictions_2019.csv")

print(cm)
print("prediction distribution", np.unique(model.predict(X[mask_test]), return_counts=True))

print("accuracy", model.score(X[mask_test], Y[mask_test]))

inds = np.argsort(-model.feature_importances_)
for i in inds:
    print("{} - {}".format(model.feature_importances_[i], X.columns[i]))



