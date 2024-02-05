from flask import Flask, render_template, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from config import key

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = key


db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    clas = db.Column(db.String(100), nullable=False)
    corpus = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


def fillingTableByUsers(users):
    for user in users:
        exists = db.session.query(db.session.query(Users).filter_by(name=user["name"]).exists()).scalar()
        if not exists:
            userdb = Users(name=user['name'], clas=user["class"], corpus=user['corpus'], state=user['state'],
                           email=user['email'])
            try:
                db.session.add(userdb)
                db.session.commit()
            except:
                print("Error!!!")

@app.route('/')
def index():
    users = db.session.query(Users).all()
    for user in users:
        if len(user.name) > 50:
            user.name = user.name[0:50] + "..."
    return render_template("index.html", users=users)

@app.route('/user/<int:id>/edit')
def editState(id):
    users = db.session.query(Users).all()
    if id < 0 or id >= len(users):
        abort(404)
    return render_template("edit.html", user=users[id], id=id)

@app.route('/user/<int:id>/came')
def change(id):
    users = db.session.query(Users).all()
    if id < 0 or id >= len(users):
        abort(404)
    state = "Пришел"
    rows = Users.query.filter_by(id=id+1).update({'state': state})
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run()