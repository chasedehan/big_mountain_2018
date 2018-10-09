"""
This script goes through:
    1) Importing and preparing data
    2) Obtaining Cross validation scores
    3) Selecting the model with the best performance
    4) Retraining model on all data
    5) Save out model as joblib object
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib

# Bring in data
titanic = pd.read_csv("http://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv")

# Select the features we want to use in the model
keep_vars = ["Pclass", "Sex", "Age"]
X = titanic[keep_vars]
y = titanic["Survived"]

# Split the categorical variables
X = pd.get_dummies(X)

# If we did more feature/model prep work, it would make sense to create a class for use in Flask
    # Could be unit tested and profiled during training time and could put into prod in little time

# Create a list of models - you can make this as complicated as you like
clfs = [GradientBoostingClassifier(),
        RandomForestClassifier(),
        AdaBoostClassifier()]

# Evaluate Performance of the Models and Select the Best Performing
print("Baseline score: {}".format(1 - (sum(y) / len(y))))
model_scores = []
for i, clf in enumerate(clfs):
    cv_scores = cross_val_score(clf, X, y, cv=5)
    mean_cv_score = cv_scores.mean()
    model_scores.append(mean_cv_score)
    print("5 Fold Accuracy clf{}: {}".format(i, mean_cv_score))

# Which model performs best?
best_model = model_scores.index(max(model_scores))

# train best model on all data to prepare for export
best_clf = clfs[best_model]
best_clf.fit(X, y)

# Save the pickle files to the file system
joblib.dump(best_clf, 'model.joblib')
joblib.dump(X.columns, 'model_columns.joblib')
# Could also have saved out a fully tested preprocessing class