from flask import Flask, render_template, redirect, request

app = Flask(__name__, static_url_path='/static')  # static url only used in development

entries = []


@app.route("/")
def show_entries():
    return render_template("show_entries.html", entries=entries)


@app.route("/add_entry", methods=['POST'])
def add_entry():
    title = request.form['title']
    text = request.form['text']
    new_entry = dict(title=title, text=text)
    entries.append(new_entry)
    return redirect('/')


@app.route("/delete")
def delete_entry():
    id = int(request.args.get('id'))
    del entries[id - 1]
    return redirect('/')


app.run(debug=True)
