from flask import Flask, g, request, redirect, render_template
import sqlite3

app = Flask(__name__, static_url_path='/static')  # static url only used in development


def get_db():
    if not hasattr(g, 'sqlite_db'):
        con = sqlite3.connect('blog.db')
        g.sqlite_db = con

    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/add_entry', methods=['POST'])
def add_entry():
    title = request.form['title']
    text = request.form['text']
    con = get_db()
    with con:
        cur = con.cursor()
        cur.execute('insert into blog values (?,?)', (title, text))
        con.commit()
    return redirect('/')


@app.route("/")
def show_entries():
    con = get_db()
    with con:
        cur = con.cursor()
        cur.execute('select rowid, * from blog')
        entries = [dict(rowid=row[0], title=row[1], text=row[2]) for row in cur.fetchall()]

    return render_template("show_entries.html", entries=entries)


@app.route("/delete")
def delete_entry():
    rowid = request.args.get('id')
    con = get_db()
    with con:
        con.execute("delete from blog where rowid = ?", str(rowid))
        con.commit()
    return redirect('/')


app.run(debug=True)
