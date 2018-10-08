# call_api.py

"""
The purpose of this file is to look like a production system, which will call the service
Potentially, this should even be a GUI running separately where you enter fields, which hits the model and
tells you if you live or die.

Yeah, I like that. Build a model using  one
"""

from flask import Flask, request, flash, render_template
import requests



app = Flask(__name__)
app.secret_key = 'super secret key'



@app.route('/testing/<value>', methods=['GET', 'POST'])
def upload_file(value):
    return value

@app.route("/", methods=['GET', 'POST'])
def waiting():
    if request.method == 'POST':

        result = {}
        result['Age'] = request.form.get('Age', type=int)
        result['Pclass'] = request.form.get('Pclass', type=int)
        result['Sex'] = request.form.get('Sex')

        r = requests.post('http://127.0.0.1:5003/', json=result)
        prediction = r.json()['prediction']
        # prediction = prediction['prediction']
        if prediction == 0:
            # return "You probably died."
            flash("You probably died")
        elif prediction == 1:
            flash("You probably lived")
            # return "You probably lived."
        else:
            flash("There was an error, it's probably your fault.")
            # return "There was an error with the request"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='localhost', port=50002)