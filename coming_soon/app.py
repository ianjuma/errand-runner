from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.errorhandler(404)
def errorHandle(e):
    return render_template('index.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(501)
def server_res(e):
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=8000, debug=False, host='127.0.0.1')
