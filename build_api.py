
###############################################################################
# Build the API Call
###############################################################################
import numpy as np
from sklearn.externals import joblib
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/testing/<value>', methods=['GET', 'POST'])
def upload_file(value):
    return value

@app.route('/', methods=('POST',))
def GetPrediction():
    if request.content_type != 'application/json':
        return 'submit as a json file'
    try:
        json_ = request.json
        print(json_)
        # Convert json into pandas to work with it
        new_X = pd.DataFrame([json_])
        # Make data look like the original training set
        new_X = pd.get_dummies(new_X)
        new_X = new_X.reindex(columns=model_columns, fill_value=0)
        print(new_X)
        # For simplicity, set up for a single observation
        prediction = clf.predict(new_X)
        # prediction is an np.array, need to convert to int to pass back as json
        prediction = np.asscalar(prediction)
        return jsonify({'prediction': prediction})

    except ValueError:
        return jsonify({'value error': 1})


if __name__ == '__main__':
    # Load up the Pickle File
    clf = joblib.load('model.pkl')
    model_columns = joblib.load('model_columns.pkl')
    app.run(port=5003)

