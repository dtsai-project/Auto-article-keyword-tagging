from flask import redirect, url_for, render_template, Blueprint, flash, request, Flask
from flask_sqlalchemy import SQLAlchemy
import forms
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from module import process
import numpy as np
import os
import re


app = Flask(__name__)
db = SQLAlchemy(app)

file_path = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.join(file_path, "data.sqlite")

app.jinja_env.filters['zip'] = zip
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + basedir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.TEXT)
    tags = db.Column(db.String)


db.create_all()


@app.route('/list-post')
def list_post():
    sto_out = []
    query = Post.query.all()
    for idx, ii in enumerate(query):
        out = []
        for i in ii.tags.split(" "):
            if '[' in i:
                pp = i.split("[")[-1]
                out.append(pp)
            elif ']' in i:
                pp = i.split("]")[0]
                out.append(pp)
            else:
                out.append(i)
        sto_out.append(out)
    num = list(range(len(query)))
    colors = ["primary", "info", "danger", "success", "warning", "light"]
    return render_template('list_post.html', forms=query, list=list, num=num, tags=sto_out, ord=ord)


@app.route('/', methods=['POST', 'GET'])
def add_post():
    form = forms.Post()
    if form.validate_on_submit():
        out = process(form.content.data)
        post = Post(
            title=form.title.data,
            content=form.content.data,
            tags=str(out)
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("list_post"))
    return render_template('add_post.html', form=form)


@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete_post(id):
    query = Post.query.get(id)
    db.session.delete(query)
    db.session.commit()
    return redirect(url_for("list_post"))


@app.route('/visualization')
def visualization():
    return render_template('list_book.html')


if __name__ == "__main__":
    app.run(debug=True)
