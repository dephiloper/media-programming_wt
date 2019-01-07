from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def say_hello():
    return "<h1>hello</h1>"


@app.route('/<name>/')
def say_hello_name(name):
    return "<h1>hello {0}</h1>".format(name)


@app.route('/template/<name>/')
def say_hello_template(name):
    return render_template('hello.html', name=name)


app.run(debug=True)
