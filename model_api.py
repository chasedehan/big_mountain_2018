import numpy as np
from sklearn.externals import joblib
from flask import Flask, request, jsonify
import pandas as pd

# Set "config" variables
PORT = 5003

app = Flask(__name__)

# Load up the models into memory
clf = joblib.load('model.joblib')
model_columns = joblib.load('model_columns.joblib')


# Create route to test if the service is up and running
@app.route('/testing/<value>', methods=['GET', 'POST'])
def upload_file(value):
    return value


# Main route to return predictions
@app.route('/', methods=('POST',))
def get_prediction():
    if request.content_type != 'application/json':
        return 'submit as a json file'
    try:
        # Convert json into pandas to work with it
        new_X = pd.DataFrame([request.json])
        # Make data look like the original training set
        new_X = pd.get_dummies(new_X)
        new_X = new_X.reindex(columns=model_columns, fill_value=0)

        # For simplicity, set up for a single observation
        # If you wanted the probability, could use: clf.predict_proba(new_X)
        prediction = clf.predict(new_X)
        # convert to int to pass back as json because comes out as np.array
        prediction = np.asscalar(prediction)

        return jsonify({'prediction': prediction})

    except ValueError:
        return jsonify({'value error': 1})


if __name__ == '__main__':
    app.run(port=PORT)