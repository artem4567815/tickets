from flask import Flask, render_template, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from main import GetUsers
from config import key
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SECRET_KEY'] = key


db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    clas = db.Column(db.String(100), nullable=False)
    corpus = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)


sendedToUsers = []

@app.route('/')
def index():
    users = GetUsers()
    return render_template("index.html", users=users)

@app.route('/user/<int:id>/edit')
def editState(id):
    users = GetUsers()
    if id < 0 or id >= len(users):
        abort(404)
    return render_template("edit.html", user=users[id], id=id)

@app.route('/user/<int:id>/came')
def change(id):
    users = GetUsers()
    if id < 0 or id >= len(users):
        abort(404)

    users[id]["state"] = "Пришел"
    return redirect('/')


if __name__ == "__main__":
    app.run()