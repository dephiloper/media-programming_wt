from flask import Flask, render_template, redirect, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__, static_url_path='/static')  # static url only used in development

app.secret_key = 'your secret'

entries = []


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    text = StringField('text', validators=[DataRequired()])


@app.route('/')
def show_entries():
    form = PostForm()
    return render_template("show_entries_wtf.html", entries=entries, form=form)


@app.route("/add_entry", methods=['POST'])
def add_entry():
    form = PostForm()

    if form.validate():
        new_entry = dict(title=form.data['title'], text=form.data['text'])
        entries.append(new_entry)
    else:
        for err in form.errors.items():
                flash(str(err))

    return redirect('/')


@app.route("/delete")
def delete_entry():
    id = int(request.args.get('id'))
    del entries[id - 1]
    return redirect('/')


app.run(debug=True)
