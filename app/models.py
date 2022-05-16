from .import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import ForeignKey


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    votes = db.relationship('Vote', backref='user', passive_deletes=True)


   
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    author= db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    votes = db.relationship('Vote', backref='post', passive_deletes=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    text = db.Column(db.String(150), nullable=False)
    author= db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey('post.id',ondelete="CASCADE"),nullable=False)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author= db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey('post.id',ondelete="CASCADE"),nullable=False)


  
