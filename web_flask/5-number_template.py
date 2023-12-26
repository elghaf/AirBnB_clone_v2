#!/usr/bin/python3
"""
script that starts a Flask web application
"""
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """This function returns Hello HBNB!"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def show_string():
    """returns HBNB"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def show_text_replace(text):
    """ Return desired string for /c/<text> route, replace '_' with space """
    text_replace = text.replace('_', ' ')
    return "C {}".format(text_replace)


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def show_text_default(text="is cool"):
    """ Return desired string for /python/<text> route
    replace '_' with space """
    text = text.replace('_', ' ')
    return "Python {}".format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def imanumber(n):
    """display “n is a number” only if n is an integer"""
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def htmlpage(n):
    """display a HTML page only if n is an integer"""
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
