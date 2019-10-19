import sys
import numpy as np
import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix
import warnings
warnings.filterwarnings("ignore")


tab = pd.read_csv("/home/administrator/repos/edufuture/data/modelling_table.csv", sep="|")

x_names_cathegorical = ['Language']
x_names_nummerical = ["Number_of_students", "cnt_olympiad_entries", 'ANG9', 'MAT9', 'MAT12', 'LAT12', 'LAT9', 'ANG12', "dist_to_nierest", "reg_iedz_skaits", "student_diff"]


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
#     model = GradientBoostingClassifier(
#         criterion="entropy",
#         max_depth=2,
#         n_estimators=100
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
model = GradientBoostingClassifier(
        # criterion="entropy",
        max_depth=5,
        n_estimators=100,
    )

# print(X)
X, Y = prepare_data(tab)
mask_train = tab.Year < 2018
mask_test = np.logical_not(mask_train)
class_weight={0: w0, 1: 1}

sample_weights = np.asarray([class_weight[c] for c in Y[mask_train]])

model.fit(X[mask_train], Y[mask_train], sample_weight=sample_weights)
preds = model.predict(X[mask_test])
cm = confusion_matrix(Y[mask_test], preds)

wacc = np.average(np.diag(cm) / np.sum(cm, axis=1))

output = pd.DataFrame({
    "school_name": tab[mask_test]["School_Name"],
    "prob_survive": model.predict_proba(X[mask_test])
})

tab["prob_survival"] = -1
tab["prob_survival"][mask_test] = model.predict_proba(X[mask_test])

output.to_csv("/home/administrator/repos/edufuture/data/school_predictions_2019.csv")

print(cm)
print("prediction distribution", np.unique(model.predict(X[mask_test]), return_counts=True))
wacc = np.average(np.diag(cm) / np.sum(cm, axis=1))
print("accuracy", model.score(X[mask_test], Y[mask_test]), wacc)

inds = np.argsort(-model.feature_importances_)
for i in inds:
    print("{} - {}".format(model.feature_importances_[i], X.columns[i]))



