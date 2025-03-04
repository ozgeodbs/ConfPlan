
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", title="Ana Sayfa")

@app.route('/agenda')
def agenda():
    return render_template("agenda.html")

@app.route('/speakers')
def speakers():
    return render_template("speakers.html")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
