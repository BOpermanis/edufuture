import sys
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

tab = pd.read_csv("/home/administrator/repos/edufuture/data/modelling_table.csv", sep="|")

x_names_cathegorical = ['Language']
x_names_nummerical = ["Number_of_students", "cnt_olympiad_entries"]

def prepare_data(tab):
    X = tab[x_names_nummerical]
    for name in x_names_cathegorical:
        x1 = pd.get_dummies(tab[name])
        for cname in x1.columns:
            X[cname] = x1[cname]
    return X, tab["Y"]

# weights = list(range(2, 30))
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

w0 = 10
model = RandomForestClassifier(
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

model.fit(X[mask_train], Y[mask_train])
preds = model.predict(X[mask_test])
cm = confusion_matrix(Y[mask_test], preds)
print(cm)
print("prediction distribution", np.unique(model.predict(X[mask_test]), return_counts=True))

print("accuracy", model.score(X[mask_test], Y[mask_test]))

inds = np.argsort(-model.feature_importances_)
for i in inds:
    print("{} - {}".format(model.feature_importances_[i], X.columns[i]))


