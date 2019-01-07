from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, Integer, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__, static_url_path='/static')  # static url only used in development

engine = create_engine('sqlite:///learning/blog.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Entry(Base):
    __tablename__ = 'blog'
    rowid = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)


Base.metadata.create_all(engine)


@app.route('/')
def show_entries():
    entries = session.query(Entry).all()
    return render_template('show_entries.html', entries=entries)


@app.route('/add_entry', methods=['POST'])
def add_entry():
    title = request.form['title']
    text = request.form['text']
    new_entry = Entry(title=title, text=text)
    session.add(new_entry)
    session.commit()
    return redirect('/')


@app.route("/delete")
def delete_entry():
    rowid = request.args.get('id')
    entry = session.query(Entry).get(rowid)
    if entry:
        session.delete(entry)
        session.commit()
    return redirect('/')


app.run(debug=True)
