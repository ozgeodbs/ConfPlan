from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("about.html", title="Ana Sayfa")

@app.route('/overview')
def about():
    return render_template("base.html", title="Program")

@app.route('/iletisim')
def contact():
    return render_template("contact.html", title="İletişim")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
