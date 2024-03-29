#!/usr/bin/python3
""" Script to start a Flask web application """

from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_world():
    """ Returns some text. """
    return 'Hello HBNB!'

@app.route('/airbnb-onepage', strict_slashes=False)
def hello_airbnb():
    """ Returns some text for the airbnb-onepage route. """
    return 'Hello HBNB!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
