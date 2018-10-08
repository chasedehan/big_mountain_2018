###############################################################################
# Train the model
###############################################################################
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score

# Bring in data and split to
titanic = pd.read_csv("http://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv")

# Select the features we want to use in the model
keep_vars = ["Pclass", "Sex", "Age"]
X = titanic[keep_vars]
y = titanic["Survived"]

# Split the categorical variables
X = pd.get_dummies(X)

# If we did more feature/model prep work, it would make sense to create a class for use in Flask
    # Could be unit tested and profiled during training time and could put into prod in little time

# Create a model
    # You can make this as complicated as you like
clf0 = GradientBoostingClassifier()
clf1 = RandomForestClassifier()
clf2 = AdaBoostClassifier()

# Evaluate Performance of the Models and Select the Best Performing
print("Baseline score: {}".format(1 - (sum(y) / len(y))))
for i, clf in enumerate([clf0, clf1, clf2]):
    cv_scores = cross_val_score(clf, X, y, cv=5)
    mean_cv_score = cv_scores.mean()
    print("5 Fold Accuracy clf{}: {}".format(i, mean_cv_score))


###############################################################################
# Save out the model object
###############################################################################
from sklearn.externals import joblib

# clf0 has the best performance so lets train on all data
clf0.fit(X, y)

# Save the pickle files to the file system
joblib.dump(clf0, 'model.pkl')
joblib.dump(X.columns, 'model_columns.pkl')
# Could also have saved out a fully tested preprocessing class


js = {'Pclass': ['2'], 'age': ['12'], 'Sex': ['male']}
response = {  "prediction": 0}

import requests
r = requests.post('http://127.0.0.1:5003/', json=js)
r.status_code
r.content
