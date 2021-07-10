
from flask import Flask, flash, jsonify, redirect, request, session,jsonify
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
import json
from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(45),nullable=False)
    password = db.Column(db.String(120),  nullable=False)
    def __repr__(self):
        return '<User %r %r %r >' % (self.id,self.username,self.email)
    def data(self):
        return{
            "id":self.id,
            "username":self.username,
            "email":self.email,
        }

@app.route("/")
def hello_world():
    return "<h1>welcome to auth service</h1>"


@app.route('/login',methods=['POST'])
def login():
    data=request.get_json()  
    res=User.query.filter(User.username == data["username"]).all()
    if len(res) != 1 or not check_password_hash(res[0].password,data["password"] ):
        return jsonify({"message":"pass/username wrong"})
    return jsonify(res[0].data())


@app.route("/register",methods=['POST'])
def Register():
    data=request.get_json()
    print(data["username"])
    checkres=User.query.filter(User.username == data["username"]).all()
    print(checkres)
    if len(checkres) > 0 :
        return jsonify({"message":"user sudah ada"}) 
    else:
        try:
            users = User(username=data["username"],email=data["email"] ,password=generate_password_hash(data["password"]))
            db.session.add(users)
            db.session.commit()
        except error:
            print(error)
            return jsonify({"message":"gagal"})
    res=User.query.filter(User.username == data["username"]).all()
    return jsonify({"message":"success"})

