from flask import Flask, request, flash, render_template
import requests

app = Flask(__name__)
app.secret_key = "some secret value"


# "config" values
PORT = 50002
URL = 'http://127.0.0.1:5003/'


# Create route to test if the service is up and running
@app.route('/testing/<value>', methods=['GET', 'POST'])
def test_running(value):
    return value


# Route to send/receive prediction
@app.route("/", methods=['GET', 'POST'])
def call_model_api():
    if request.method == 'POST':

        # Build dict to pass as json
        result = {'Age': request.form.get('Age', type=int),
                  'Pclass': request.form.get('Pclass', type=int),
                  'Sex': request.form.get('Sex')}

        # Make the request to the model API
        r = requests.post(URL, json=result)
        prediction = r.json()['prediction']
        probability = r.json()['probability']

        # Check the predictions and return the result
        if prediction == 0:
            flash("You probably died, with a probability of dying: {:.4f}".format(probability))
        elif prediction == 1:
            flash("You probably lived, with a probability of dying: {:.4f}".format(probability))
        else:
            flash("There was an error, it's probably your fault.")

    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=PORT)